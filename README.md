<p align="center">
<img src="https://github.com/QualiSystems/devguide_source/raw/master/logo.png"></img>
</p>

# **Palo Alto Firewall Static Shell**  

Release date: **September 2018**

Shell version: **1.0.0**

Document version: **1.0.0**

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Typical Workflow and Scenarios](#typical-workflow-and-scenarios)
* [References](#references)


# Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

### Firewall Shells
CloudShell's Firewall shells enable you to manage your Firewall device similar to your networking equipment but without connectivity. In CloudShell, a Firewall shell runs commands, such as Autoload, Load, and Save Configuration. 

### **Palo Alto Firewall Static Shell**
The **Palo Alto Firewall Static Shell** provides you with connectivity and management capabilities such as device structure discovery and power management for the **Palo Alto Firewall**. 

For more information on the **Palo Alto Firewall**, see the official **Palo Alto** product documentation.

### Standard version
The **Palo Alto Firewall Static Shell 1.0.0** is based on the Deployed App Shell Standard version 1.0.3.

For detailed information about the shell’s structure and attributes, see the [Deployed App Shell Standard](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/deployed_app_standard.md) in GitHub.

### Supported OS
▪ **PanOS**

### Requirements

Release: **Palo Alto Firewall Static Shell 1.0.0**

* CloudShell version 8.3 (with the latest patch) and above

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **Palo Alto Static Firewall Families and Models**

The chassis families and models are listed in the following table:

|Family|Model|Description|
|:---|:---|:---|
|CS_GenericAppFamily|PaloAlto Static vFirewall|Static Virtual PaloAlto Firewall|
|CS_Port|PaloAlto Static vFirewall.GenericVPort|Generic Virtual Port|

### Automation
The following commands are associated with the Palo Alto Firewall Static shell:

|Command|Description|
|:-----|:-----|
|Health Check|Checks if the device is powered-on and connectable.|
|Send Custom Command|Executes a custom command on the device. <br>Command Inputs:</br><li>**Command**: The command to run. Note that commands that require a response are not supported.</br>|
|Save|Creates a configuration file and saves it to the provided destination.<br>Command Inputs:</br><li>**Folder Path**: Path where the configuration file will be saved. It should be accessible from the execution server. The path should include the protocol type, for example: tftp://asdf.</br><li>**Configuration Type**: Specify whether the file should update the Startup or Running config.<br>- Startup: Configuration that is loaded when the device boots or powers up. Startup configuration is not supported on all switches.<br>- Running: Current configuration in the device. It may have been modified since the last boot.|
|Restore|Restores a configuration from the saved file.<br>Command Inputs:</br><li>**Path**: The full path from which the configuration file will be restored. The path should include the protocol type, for example: tftp://asdf.</br><li>**Configuration Type**: Specify whether the file should update the Startup or Running config.<br>- Startup: Configuration that is loaded when the device boots or powers up. Startup configuration is not supported on all switches.<br>- Running: Current configuration in the device. It may have been modified since the last boot.<br><li>**Restore Method**: Determines whether the restore should append or override the current configuration.|
|Load Firmware|Uploads and updates the firmware on the resource. <br>Command Inputs:</br><li>**Path**: Path to tftp://server where the firmware file is stored.|
	
# Downloading the Shell
The **Palo Alto Firewall Static Shell** is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises:

|File name|Description|
|:---|:---|
|PaloAltoStaticFirewallShell.zip|Palo Alto Firewall Static shell package|
|cloudshell-firewall-paloalto-dependencies-package-1.0.0.zip|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the **Palo Alto Firewall Static Shell** and configure and modify the shell’s devices.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  2. In CloudShell Portal, as Global administrator, open the **Manage – Shells** page.
  3. Click **Import**.
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**.

The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. 

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offlinemode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Configuring a new resource
This section explains how to create a new resource from the shell.

In CloudShell, the component that models the device is called a resource. It is based on the shell that models the device and allows the CloudShell user and API to remotely control the device from CloudShell.

You can also modify existing resources, see [Managing Resources in the Inventory](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Mng-Rsrc-in-Invnt.htm?Highlight=managing%20resources).

**To create a resource for the device:**
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**. 
     ![](https://github.com/QualiSystems/PaloAlto-PanoOS-Static-Shell/blob/master/docs/create_a_resource_device.png)
  2. From the list, select **Palo Alto Firewall Static** shell.
  3. Enter the **Name** and **IP address** (if applicable).
  4. Click **Create**.
  5. In the **Resource** dialog box, enter the device's settings, as required. See [Palo Alto Static Firewall Attributes](#palo-alto-static-firewall-attributes).
   6. Click **Continue**.

CloudShell validates the device’s settings and updates the new resource with the device’s structure (if the device has a structure).

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.

### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.
2. Extract the zip file to the suitable offline package folder(s). 
3. Restart any execution server that has a live instance of the relevant driver or script. This requires running the Execution Server's configuration wizard, as explained in the [Configure the Execution Server](http://help.quali.com/doc/9.0/CS-Install/content/ig/configure%20cloudshell%20products/cfg-ts-exec-srver.htm?Highlight=configure%20the%20execution%20server) topic of the CloudShell Suite Installation guide. 

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, restart the execution server, as explained above. If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

### **Palo Alto Static Firewall Attributes**

The attribute names and types are listed in the following table. 

**Note:** All attributes appear both in the **Edit** resource dialog box (Inventory>Resource>Edit) and the **Discover** resource dialog box (Inventory>Resource>Discover) except for those noted with an *, which appear only in the **Edit** resource dialog box. 

|Attribute|Type|Default value|Description|
|:---|:---|:---|:---|
|Name*|String||CloudShell resource display name|
|Address*|String||Resource address (address of the device)|
|Folder*|String|Root|CloudShell folder in which to place the resource. Use the search bar to quickly find the desired folder.|
|Visibility*|Lookup|Family Default (Everyone)|Visibility determines who can see the resource in the diagram, search pane, and in the **Inventory** dashboard.  By default the visibility is defined in the resource family and can be changed for a specific resource.<br>Possible values: **Family Default (Everyone)**, **Admin only**, and **Everyone**.|
|Remote Connection*|Lookup|Family Default (Enable)|Remote connection determines if can remotely connect to the resource. By default the Remote Connection is defined in the resource family and can be changed for a specific resource.<br> Possible values: **Family Default (Enable)**, **Enable**, and **Disable**.|
|vFirewall VCenter Name|String||Virtual Firewall vCenter VM to use in VM creation. <br>Should include the full path and the VM name, for example: *QualiFolder/VM121*.|
|vCenter Name|String||The vCenter resource name in CloudShell.|
|Sessions Concurrency Limit|Numeric|1|Maximum number of concurrent sessions that the driver can open to the device. <br>Defines the number of commands that can run concurrently. <br>Default value of 1 = no concurrent sessions.|
|CLI Connection Type|Lookup|Auto|The CLI connection type that will be used by the driver. <br>Possible values: **Auto**, **Console**, **SSH**, **Telnet** and **TCP**. If **Auto** is selected the driver will choose the available connection type automatically.|
|CLI TCP Port|Numeric||TCP Port for CLI connection. <br>If empty, a default CLI port will be used based on the chosen protocol. <br>For example, Telnet will use port 23.|
|Backup Location|String||Used by the save/restore orchestration to determine where backups should be saved.|
|Backup Type|String|File System|Supported protocols for saving and restoring configuration and firmware files. <br>Possible values: **File System**, **FTP**, and **TFTP**.|
|Backup User|String||User name for the storage server used for saving and restoring the configuration and firmware files.|
|Backup Password|Password||Password for the storage server used for saving and restoring the configuration and firmware files.|
|User|String||User name for the Palo Alto Firewall CLI (should be a privileged user)|
|Password|Password||Password for Palo Alto Firewall CLI|
Public IP*|String|||

# Typical Workflow and Scenarios 

**Scenario 1 - _Save configuration_** 
1. In CloudShell Portal, add the device resource to an active sandbox.
2. Run the **Save** command on the device with the following inputs:
    * **Folder Path**: For example, *tftp://ipaddress/shared folder* 
    * **Configuration Type**: **Running** or **Startup**

The configuration is saved to a file named *<ResourceName><startup/running-config>-<timestamp>*, which will reside in the folder path you entered.    

**Scenario 2 - _Restore Configuration_**
1. In CloudShell Portal, reserve the device resource.
2. Run the **Restore** resource command.
3. Enter the following parameters:
    * **Path** (mandatory): Enter the full path of the configuration file. 
    * **Restore Method** (optional): **Append** or **Override**. If you do not enter any value in this field, the **Append** method will be used. 
    * **Configuration Type** (mandatory): **Startup** or **Running**. 
	
**Scenario 3 - _Load firmware_**
1. In CloudShell Portal, reserve the device resource.
2. Run the **Load Firmware** resource command.
3. Enter the following parameters:
    * **Path** (mandatory): Enter the full path of the firmware file on the remote host. For example, *tftp://10.1.1.1/PanOS_200-5.0.5*.
   
# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation resources, see the [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 
