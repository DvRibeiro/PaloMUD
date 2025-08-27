import asyncio
from constants_util import NAME_VERSION
import telnetlib3
from rich.console import Console
from rich.panel import Panel
from shell_factory import ShellFactory

console = Console()

async def main(host="0.0.0.0", port=2323):
    shell_object = ShellFactory.return_shell()
    shell = shell_object.shell  

    server = await telnetlib3.create_server(
        host=host,
        port=port,
        shell=shell,
        encoding="utf-8",   # força UTF-8 para todos os clientes que suportam
        connect_maxwait=3,
    )

    console.print(Panel(f"[bold green]>> {NAME_VERSION} | Servidor Telnet ouvindo em {host}:{port}[/bold green]"))
    console.print("[red]Aviso:[/red] [bold]Pressione Ctrl+C para sair[/bold].")

    try:
        await server.wait_closed()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    asyncio.run(main())
