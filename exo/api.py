from exo.orchestration.node import Node
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
import uuid
import uvicorn
import os
import requests

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

node: Optional[Node] = None
roxonn_wallet_address: Optional[str] = None
node_host: Optional[str] = None
node_port: Optional[int] = None

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
                if tokens and tokens[-1] == tokenizer.eos_token_id:
                    tokens = tokens[:-1]
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

async def send_heartbeat(node_id, wallet_address, host, port):
    # First, check if the node is registered on-chain
    try:
        check_url = f"https://api.roxonn.com/api/node/check-registration?nodeId={node_id}"
        response = requests.get(check_url)
        if not response.json().get("isRegistered"):
            print("Node not registered on-chain. Attempting to register...")
            register_url = "https://api.roxonn.com/api/node/register"
            register_payload = {"nodeId": node_id, "walletAddress": wallet_address}
            register_response = requests.post(register_url, json=register_payload)
            if register_response.status_code == 200:
                print("Node successfully registered on-chain.")
            else:
                print(f"Failed to register node on-chain: {register_response.text}")
    except Exception as e:
        print(f"Error during node registration check: {e}")

    while True:
        try:
            payload = {
                "node_id": node_id,
                "wallet_address": wallet_address,
                "ip_address": host,
                "port": port
            }
            roxonn_url = os.environ.get("ROXONN_HEARTBEAT_URL", "https://api.roxonn.com/api/node/heartbeat")
            requests.post(roxonn_url, json=payload)
            if "DEBUG" in os.environ and os.environ["DEBUG"] >= 1: print(f"Sent heartbeat for node {node_id}")
        except Exception as e:
            if "DEBUG" in os.environ and os.environ["DEBUG"] >= 1: print(f"Failed to send heartbeat: {e}")
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    if roxonn_wallet_address:
        asyncio.create_task(send_heartbeat(node.id, roxonn_wallet_address, node_host, node_port))

async def run(node_instance: Node, host="0.0.0.0", port=52415):
    global node
    node = node_instance
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
