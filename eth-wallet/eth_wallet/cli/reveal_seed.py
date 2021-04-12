import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.exceptions import (
    InvalidPasswordException,
)


@click.command()
@click.option('-p', '--password', default='', prompt='Password:',
              help='Your Ethereum wallet password.')
def reveal_seed(password):
    """Reveals private key from encrypted keystore."""

    configuration = Configuration().load_configuration()
    api = get_api()

    try:
        wallet = api.get_private_key(configuration, password)
        click.echo('Account prv key: %s' % str(wallet.get_private_key().hex()))

    except InvalidPasswordException:
        click.echo('Incorrect password!')
