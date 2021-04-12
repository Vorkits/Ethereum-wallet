import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)


@click.command()
@click.option('-p', '--password', default='', prompt='Password:',
              help='Enter your password to create your wallet.')
def new_wallet(password):
    """Creates new wallet and store encrypted keystore file."""

    configuration = Configuration().load_configuration()

    api = get_api()
    wallet = api.new_wallet(configuration, password)

    click.echo('Account address: %s' % str(wallet.get_address()))
    click.echo('Account pub key: %s' % str(wallet.get_public_key()))
    click.echo('Keystore path: %s' % configuration.keystore_location + configuration.keystore_filename)
    click.echo('Remember these words to restore eth-wallet: %s' % wallet.get_mnemonic())




