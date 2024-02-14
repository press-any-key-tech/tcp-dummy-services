import asyncio
import argparse

from tcp_dummy_services.core import logger, settings
import sys


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    addr_socket = writer.get_extra_info("sockname")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            message = data.decode().strip()
            if message in ("END", "QUIT", "EXIT", "ADIOS", "BYE"):
                break

            logger.info(f"Received message from {addr} in {addr_socket}: {message}")

            writer.write(data)
            await writer.drain()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info(f"Closing the connection on {addr} / {addr_socket}")
        writer.close()
        await writer.wait_closed()


async def start_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)

    addr = server.sockets[0].getsockname()
    logger.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


async def main(host, start_port, end_port):
    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(asyncio.create_task(start_server(host, port)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # TODO: Change argument parsing to another function
    parser = argparse.ArgumentParser(description="Asyncion TCP Server")

    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="The host to start the server on. Default is 0.0.0.0",
    )

    args = parser.parse_args()

    # Check if ports argument is a range or a single port
    if "-" in settings.TCP_PORTS:
        start_port, end_port = map(int, settings.TCP_PORTS.split("-"))
    else:
        start_port = end_port = int(settings.TCP_PORTS)

    try:
        asyncio.run(main(args.host, start_port, end_port))
    except KeyboardInterrupt:
        # Get all running tasks:
        tasks = asyncio.all_tasks()
        for task in tasks:
            task.cancel()
        # Wait until all tasks are cancelled:
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*tasks, return_exceptions=True)
        )
        logger.info("Server shut down.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
