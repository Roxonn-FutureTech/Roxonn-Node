from exo.orchestration.node import Node
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Optional
import asyncio
import json
import time
import uuid

class ChatGPTAPI:
    def __init__(
        self,
        node: Node,
        inference_engine_name: str,
        response_timeout: int = 900,
        on_chat_completion_request: Optional[callable] = None,
        default_model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ):
        self.app = FastAPI()
        self.node = node
        self.inference_engine_name = inference_engine_name
        self.response_timeout = response_timeout
        self.on_chat_completion_request = on_chat_completion_request
        self.default_model = default_model
        self.system_prompt = system_prompt
        self.setup_routes()

    def setup_routes(self):
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

        @self.app.post("/execute-task")
        async def execute_task(request: Request):
            print("Received compute task from Roxonn dispatcher...")
            try:
                request_data = await request.json()
                prompt = request_data["prompt"]
                
                # This is a simplified version of the logic in the main run_model_cli.
                # A helper function in the Node class would be a cleaner implementation.
                shard = self.node.inference_engine.shard
                if not shard:
                    return {"status": "error", "message": "Node has no model loaded."}

                tokenizer = self.node.inference_engine.tokenizer
                request_id = str(uuid.uuid4())
                
                # We need a way to get the response back. We'll create a future for it.
                future = asyncio.get_event_loop().create_future()

                def on_token_callback(req_id, tokens, is_finished):
                    if req_id == request_id and is_finished:
                        response_text = tokenizer.decode(tokens)
                        future.set_result(response_text)

                callback_id = f"task-response-{request_id}"
                self.node.on_token.register(callback_id).on_next(on_token_callback)

                formatted_prompt = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
                await self.node.process_prompt(shard, formatted_prompt, request_id=request_id)

                response_text = await asyncio.wait_for(future, timeout=self.response_timeout)
                self.node.on_token.deregister(callback_id)

                print("Compute task finished.")
                return {"status": "task complete", "response": response_text}
            except Exception as e:
                print(f"Error during compute task: {e}")
                return {"status": "error", "message": str(e)}

    async def run(self, host="0.0.0.0", port=52415):
        import uvicorn
        config = uvicorn.Config(self.app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
