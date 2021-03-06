""" The config-set-celery-broker-url command. """

from .base import Base, config_editor

class ConfigSetCeleryBrokerUrl(Base):
    """ Set Celery Broker URL to config """

    def run(self):
        config = config_editor.ConfigEditor(self.config_path)
        value = self.options.get("<value>")
        config.parse()
        config.parsed.set_celery_broker_url(value)
        config.parsed_to_content()
        config.save()
