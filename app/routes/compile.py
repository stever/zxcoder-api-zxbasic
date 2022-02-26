import tempfile
import base64
import os
from pathlib import Path
from src.zxbc import main
from fastapi import APIRouter, Header
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class SessionVars(BaseModel):
    x_hasura_role: str = Field(alias="x-hasura-role")
    x_hasura_user_id: Optional[UUID] = Field(alias="x-hasura-user-id")


class Input(BaseModel):
    basic: str


class Action(BaseModel):
    name: str


class RequestArgs(BaseModel):
    session_variables: SessionVars
    input: Input
    action: Action


class CompileResult(BaseModel):
    base64_encoded: str


compile_endpoint = APIRouter()


@compile_endpoint.post("/", response_model=CompileResult)
def handle_compile_request(
        args: RequestArgs,
        authorization: Optional[str] = Header(None)) -> Optional[CompileResult]:

    # user_id = args.session_variables.x_hasura_user_id
    # role = args.session_variables.x_hasura_role

    # Write ZX Basic to file.
    tmp = tempfile.NamedTemporaryFile()
    bas_filename = f'{tmp.name}.bas'
    with open(bas_filename, 'w') as f:
        f.write(args.input.basic)

    # Compile the tape file from basic source.
    main(['-taB', bas_filename])

    # Read and base64 encode the binary tape file.
    tap_filename = f'{Path(bas_filename).stem}.tap'
    with open(tap_filename, 'rb') as f:
        base64_encoded = base64.b64encode(f.read()).decode()
        os.remove(bas_filename)
        os.remove(tap_filename)
        return CompileResult(base64_encoded=base64_encoded)
