from __future__ import annotations

from cloudshell.shell.core.driver_context import (
    AutoLoadCommandContext,
    AutoLoadDetails,
    ResourceCommandContext,
)

from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.session_pool_manager import SessionPoolManager
from cloudshell.shell.core.driver_context import InitCommandContext
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.orchestration_save_restore import OrchestrationSaveRestore
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.flows.command.basic_flow import RunCommandFlow
from cloudshell.shell.standards.firewall.autoload_model import FirewallResourceModel
from cloudshell.shell.standards.firewall.driver_interface import (
    FirewallResourceDriverInterface,
)
from cloudshell.shell.standards.firewall.resource_config import FirewallResourceConfig
from cloudshell.snmp.snmp_configurator import EnableDisableSnmpConfigurator

from cloudshell.firewall.paloalto.panos.cli.panos_cli_configurator import (
    PanOSCliConfigurator,
)
from cloudshell.firewall.paloalto.panos.flows.panos_autoload_flow import (
    PanOSSnmpAutoloadFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_configuration_flow import (
    PanOSConfigurationFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_enable_disable_snmp_flow import (
    PanOSEnableDisableSnmpFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_load_firmware_flow import (
    PanOSLoadFirmwareFlow,
)
from cloudshell.firewall.paloalto.panos.flows.panos_state_flow import PanOSStateFlow


class PaloAltoShellDriver(ResourceDriverInterface, FirewallResourceDriverInterface):
    SUPPORTED_OS = [r"Palo Alto"]
    SHELL_NAME = "PaloAlto PanOS Firewall Shell 2G"

    def __init__(self):
        self._cli = None

    def initialize(self, context: InitCommandContext) -> str:
        api = CloudShellSessionContext(context).get_api()
        resource_config = FirewallResourceConfig.from_context(context, api)
        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = CLI(
            SessionPoolManager(max_pool_size=session_pool_size, pool_timeout=100)
        )
        return "Finished initializing"

    def health_check(self, context: ResourceCommandContext) -> str:
        """Performs device health check."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            state_operations = PanOSStateFlow(resource_config, cli_configurator, api)
            return state_operations.health_check()

    @GlobalLock.lock
    def get_inventory(self, context: AutoLoadCommandContext) -> AutoLoadDetails:
        """Return device structure with all standard attributes."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)

            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )
            enable_disable_snmp_flow = PanOSEnableDisableSnmpFlow(cli_configurator)
            snmp_configurator = EnableDisableSnmpConfigurator.from_config(
                enable_disable_snmp_flow, resource_config, logger
            )

            resource_model = FirewallResourceModel.from_resource_config(resource_config)

            autoload_operations = PanOSSnmpAutoloadFlow(snmp_configurator)
            logger.info("Autoload started")
            response = autoload_operations.discover(self.SUPPORTED_OS, resource_model)
            logger.info("Autoload completed")
            return response

    def run_custom_command(
            self,
            context: ResourceCommandContext,
            custom_command: str
    ) -> str:
        """Send custom command."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            send_command_operations = RunCommandFlow(cli_configurator)
            response = send_command_operations.run_custom_command(custom_command)
            return response

    def run_custom_config_command(
            self,
            context: ResourceCommandContext,
            custom_command: str
    ) -> str:
        """Send custom command in configuration mode."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            send_command_operations = RunCommandFlow(cli_configurator)
            result_str = send_command_operations.run_custom_config_command(
                custom_command
            )
            return result_str

    def save(
            self,
            context: ResourceCommandContext,
            folder_path: str,
            configuration_type: str,
            vrf_management_name: str,
    ) -> str:
        """Save selected file to the provided destination."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            if not configuration_type:
                configuration_type = "running"

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            configuration_operations = PanOSConfigurationFlow(
                resource_config, cli_configurator
            )
            logger.info("Save started")
            response = configuration_operations.save(
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
        """Restore selected file to the provided destination."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            if not configuration_type:
                configuration_type = "running"

            if not restore_method:
                restore_method = "override"

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            configuration_operations = PanOSConfigurationFlow(
                resource_config, cli_configurator
            )
            logger.info("Restore started")
            configuration_operations.restore(
                path=path,
                restore_method=restore_method,
                configuration_type=configuration_type,
                vrf_management_name=vrf_management_name,
            )
            logger.info("Restore completed")


    @GlobalLock.lock
    def load_firmware(
            self,
            context: ResourceCommandContext,
            path: str,
            vrf_management_name: str
    ):
        """Upload and updates firmware on the resource."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            logger.info("Start Load Firmware")
            firmware_operations = PanOSLoadFirmwareFlow(
                resource_config,
                cli_configurator
            )
            firmware_operations.load_firmware(
                path=path, vrf_management_name=vrf_management_name
            )
            logger.info("Finish Load Firmware")

    def shutdown(self, context: ResourceCommandContext):
        """Shutdown device."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            state_operations = PanOSStateFlow(resource_config, cli_configurator, api)

            return state_operations.shutdown()

    def orchestration_save(
            self,
            context: ResourceCommandContext,
            mode: str,
            custom_params: str
    ) -> str:
        """Save selected file to the provided destination."""
        if not mode:
            mode = "shallow"

        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            configuration_operations = PanOSConfigurationFlow(
                resource_config, cli_configurator
            )

            logger.info("Orchestration save started")
            response = configuration_operations.orchestration_save(
                mode=mode, custom_params=custom_params
            )
            response_json = OrchestrationSaveRestore(
                resource_config.name
            ).prepare_orchestration_save_result(response)
            logger.info("Orchestration save completed")
            return response_json

    def orchestration_restore(
            self,
            context: ResourceCommandContext,
            saved_artifact_info: str,
            custom_params: str,
    ):
        """Restore selected file to the provided destination."""
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = FirewallResourceConfig.from_context(context, api)
            cli_configurator = PanOSCliConfigurator.from_config(
                resource_config, logger, self._cli
            )

            configuration_operations = PanOSConfigurationFlow(
                resource_config, cli_configurator
            )

            logger.info("Orchestration restore started")
            restore_params = OrchestrationSaveRestore(
                resource_config.name
            ).parse_orchestration_save_result(saved_artifact_info, custom_params)
            configuration_operations.restore(**restore_params)
            logger.info("Orchestration restore completed")

    def cleanup(self):
        """Destroy the driver session.

        This function is called everytime a driver instance is destroyed.
        This is a good place to close any open sessions, finish writing to log files
        """
        pass
