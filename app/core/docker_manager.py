import json
import docker
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()

    def execute_code(self, code: str) -> Dict:
        try:
            container = self.client.containers.create(
                'runner:latest',
                stdin_open=True,
                tty=True,
                network_mode='none',
                mem_limit='128m',
                memswap_limit='256m',
                cpu_period=100000,
                cpu_quota=50000
            )

            try:
                container.start()

                result = container.exec_run(
                    cmd=["python", "-c", code],
                    demux=True
                )

                stdout = result.output[0].decode('utf-8') if result.output[0] else ''
                stderr = result.output[1].decode('utf-8') if result.output[1] else ''

                return {
                    "success": result.exit_code == 0,  # True if exit code is 0
                    "output": stdout.strip(),  # Remove extra whitespace
                    "error": stderr.strip() if stderr else None  # Only include error if there is one
                }
            finally:
                try:
                    container.stop()
                    container.remove()
                except:
                    logger.error("Failed to cleanup container")
        except Exception as e:
            logger.error(f"Docker execution error: {str(e)}")

            return {
                "success": False,
                "error": str(e),
                "output": ""
            }