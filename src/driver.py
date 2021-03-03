#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.shell.core.driver_context import (
    AutoLoadCommandContext,
    AutoLoadDetails,
    InitCommandContext,
    ResourceCommandContext,
)
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.orchestration_save_restore import OrchestrationSaveRestore
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.standards.firewall.autoload_model import FirewallResourceModel
from cloudshell.shell.standards.firewall.driver_interface import (
    FirewallResourceDriverInterface,
)
from cloudshell.shell.standards.firewall.resource_config import (
    FirewallResourceConfig,
)


from cloudshell.firewall.paloalto.panos.cli.panos_cli_handler import PanOSCli
from cloudshell.firewall.paloalto.panos.flows.panos_autoload_flow import (
    PanOSSnmpAutoloadFlow as AutoloadFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_configuration_flow import (
    PanOSConfigurationFlow as ConfigurationFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_load_firmware_flow import (
    PanOSLoadFirmwareFlow as FirmwareFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_run_command_flow import (
    PanOSRunCommandFlow as CommandFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_state_flow import (
    PanOSStateFlow as StateFlow,
)
from cloudshell.firewall.paloalto.panos.snmp.panos_snmp_handler import (
    PanOSSnmpHandler as SNMPHandler,
)


class PaloAltoShellDriver(
    ResourceDriverInterface, FirewallResourceDriverInterface, GlobalLock
):
    SUPPORTED_OS = [r"Palo Alto"]
    SHELL_NAME = "PaloAlto PanOS Firewall Shell 2G"

    def __init__(self):
        super(PaloAltoShellDriver, self).__init__()
        self._cli = None

    def initialize(self, context: InitCommandContext) -> str:
        """Initialize method.
        :param context: an object with all Resource Attributes inside
        """
        resource_config = FirewallResourceConfig.from_context(
            shell_name=self.SHELL_NAME, supported_os=self.SUPPORTED_OS, context=context
        )

        self._cli = PanOSCli(resource_config)
        return "Finished initializing"

    def health_check(self, context: ResourceCommandContext):
        """Performs device health check.
        :param context: an object with all Resource Attributes inside
        :return: Success or Error message
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )
            cli_handler = self._cli.get_cli_handler(resource_config, logger)

            state_operations = StateFlow(
                logger=logger,
                api=api,
                resource_config=resource_config,
                cli_configurator=cli_handler,
            )
            return state_operations.health_check()

    @GlobalLock.lock
    def get_inventory(self, context: AutoLoadCommandContext) -> AutoLoadDetails:
        """Return device structure with all standard attributes.
        :param context: an object with all Resource Attributes inside
        :return: response
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )
            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            snmp_handler = SNMPHandler(resource_config, logger, cli_handler)

            autoload_operations = AutoloadFlow(logger=logger, snmp_handler=snmp_handler)
            logger.info("Autoload started")
            resource_model = FirewallResourceModel(
                resource_config.name,
                resource_config.shell_name,
                resource_config.family_name,
            )

            response = autoload_operations.discover(
                resource_config.supported_os, resource_model
            )
            logger.info("Autoload completed")
            return response

    def run_custom_command(
        self, context: ResourceCommandContext, custom_command: str
    ) -> str:
        """Send custom command.
        :param custom_command: Command user wants to send to the device.
        :param context: an object with all Resource Attributes inside
        :return: result
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            send_command_operations = CommandFlow(
                logger=logger, cli_configurator=cli_handler
            )

            response = send_command_operations.run_custom_command(
                custom_command=custom_command
            )

            return response

    def run_custom_config_command(
        self, context: ResourceCommandContext, custom_command: str
    ) -> str:
        """Send custom command in configuration mode.
        :param custom_command: Command user wants to send to the device
        :param context: an object with all Resource Attributes inside
        :return: result
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            send_command_operations = CommandFlow(
                logger=logger, cli_configurator=cli_handler
            )

            result_str = send_command_operations.run_custom_config_command(
                custom_command=custom_command
            )

            return result_str

    def save(
        self,
        context: ResourceCommandContext,
        folder_path: str,
        configuration_type: str,
        vrf_management_name: str,
    ) -> str:
        """Save selected file to the provided destination.
        :param context: an object with all Resource Attributes inside
        :param configuration_type: source file, which will be saved
        :param folder_path: destination path where file will be saved
        :param vrf_management_name: VRF management Name
        :return str saved configuration file name
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            if not configuration_type:
                configuration_type = "running"

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            configuration_flow = ConfigurationFlow(
                cli_handler=cli_handler, logger=logger, resource_config=resource_config
            )
            logger.info("Save started")
            response = configuration_flow.save(
                folder_path=folder_path,
                configuration_type=configuration_type,
                vrf_management_name=vrf_management_name,
            )
            logger.info("Save completed")
            return response

    @GlobalLock.lock
    def restore(
        self,
        context: ResourceCommandContext,
        path: str,
        configuration_type: str,
        restore_method: str,
        vrf_management_name: str,
    ):
        """Restore selected file to the provided destination.
        :param context: an object with all Resource Attributes inside
        :param path: source config file
        :param configuration_type: running or startup configs
        :param restore_method: append or override methods
        :param vrf_management_name: VRF management Name
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            if not configuration_type:
                configuration_type = "running"

            if not restore_method:
                restore_method = "override"

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            configuration_flow = ConfigurationFlow(
                cli_handler=cli_handler, logger=logger, resource_config=resource_config
            )
            logger.info("Restore started")
            configuration_flow.restore(
                path=path,
                restore_method=restore_method,
                configuration_type=configuration_type,
                vrf_management_name=vrf_management_name,
            )
            logger.info("Restore completed")

    @GlobalLock.lock
    def load_firmware(
        self, context: ResourceCommandContext, path: str, vrf_management_name: str
    ):
        """Upload and updates firmware on the resource.
        :param context: an object with all Resource Attributes inside
        :param path: full path to firmware file, i.e. tftp://10.10.10.1/firmware.tar
        :param vrf_management_name: VRF management Name
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            cli_handler = self._cli.get_cli_handler(resource_config, logger)

            logger.info("Start Load Firmware")
            firmware_operations = FirmwareFlow(cli_handler=cli_handler, logger=logger)
            response = firmware_operations.load_firmware(
                path=path, vrf_management_name=vrf_management_name
            )
            logger.info("Finish Load Firmware: {}".format(response))

    def shutdown(self, context: ResourceCommandContext):
        """Shutdown device.
        :param context: an object with all Resource Attributes inside
        :return:
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            state_operations = StateFlow(
                logger=logger,
                api=api,
                resource_config=resource_config,
                cli_configurator=cli_handler,
            )

            return state_operations.shutdown()

    def orchestration_save(
        self, context: ResourceCommandContext, mode: str, custom_params: str
    ) -> str:
        """Save selected file to the provided destination.
        :param context: an object with all Resource Attributes inside
        :param mode: mode
        :param custom_params: json with custom save parameters
        :return str response: response json
        """
        with LoggingSessionContext(context) as logger:
            if not mode:
                mode = "shallow"

            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            configuration_flow = ConfigurationFlow(
                cli_handler=cli_handler, logger=logger, resource_config=resource_config
            )

            logger.info("Orchestration save started")
            response = configuration_flow.orchestration_save(
                mode=mode, custom_params=custom_params
            )
            response_json = OrchestrationSaveRestore(
                logger, resource_config.name
            ).prepare_orchestration_save_result(response)
            logger.info("Orchestration save completed")
            return response_json

    def orchestration_restore(
        self,
        context: ResourceCommandContext,
        saved_artifact_info: str,
        custom_params: str,
    ):
        """Restore selected file to the provided destination.
        :param context: an object with all Resource Attributes inside
        :param saved_artifact_info: OrchestrationSavedArtifactInfo json
        :param custom_params: json with custom restore parameters
        """

        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(
                shell_name=self.SHELL_NAME,
                supported_os=self.SUPPORTED_OS,
                context=context,
                api=api,
            )

            cli_handler = self._cli.get_cli_handler(resource_config, logger)
            configuration_flow = ConfigurationFlow(
                cli_handler=cli_handler, logger=logger, resource_config=resource_config
            )

            logger.info("Orchestration restore started")
            restore_params = OrchestrationSaveRestore(
                logger, resource_config.name
            ).parse_orchestration_save_result(saved_artifact_info)
            configuration_flow.restore(**restore_params)
            logger.info("Orchestration restore completed")

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass
