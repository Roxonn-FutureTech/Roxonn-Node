from exo.orchestration.node import Node
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
import uuid
import uvicorn

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

node: Optional[Node] = None

@app.post("/execute-task")
async def execute_task(request: Request):
    print("Received compute task from Roxonn dispatcher...")
    try:
        request_data = await request.json()
        prompt = request_data["prompt"]
        
        if not node:
            return {"status": "error", "message": "Node not initialized."}

        shard = node.inference_engine.shard
        if not shard:
            return {"status": "error", "message": "Node has no model loaded."}

        tokenizer = node.inference_engine.tokenizer
        request_id = str(uuid.uuid4())
        
        future = asyncio.get_event_loop().create_future()

        def on_token_callback(req_id, tokens, is_finished):
            if req_id == request_id and is_finished:
                response_text = tokenizer.decode(tokens)
                future.set_result(response_text)

        callback_id = f"task-response-{request_id}"
        node.on_token.register(callback_id).on_next(on_token_callback)

        formatted_prompt = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        await node.process_prompt(shard, formatted_prompt, request_id=request_id)

        response_text = await asyncio.wait_for(future, timeout=900)
        node.on_token.deregister(callback_id)

        print("Compute task finished.")
        return {"status": "task complete", "response": response_text}
    except Exception as e:
        print(f"Error during compute task: {e}")
        return {"status": "error", "message": str(e)}

async def run(host="0.0.0.0", port=52415):
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
