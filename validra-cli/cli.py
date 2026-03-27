import click
from client import run_test
import yaml


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file")
def run(file):
    """Run a Validra test from YAML file"""

    with open(file) as f:
        config = yaml.safe_load(f)

    click.echo("🚀 Running Validra test...\n")

    results = run_test(config)

    for i, result in enumerate(results, 1):
        click.echo(f"--- Test #{i} ---")
        click.echo(f"Payload: {result['payload']}")
        click.echo(f"Status: {result['response']['status_code']}")
        click.echo(f"Valid: {result['validation'].get('valid')}")
        click.echo("")

    click.echo("✅ Done")


if __name__ == "__main__":
    cli()