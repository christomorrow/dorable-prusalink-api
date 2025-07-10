__all__ = ['Printer']

from typing import Any, BinaryIO, Optional, Union, List

from dorable_3dprinter_api import (
    IPrinter, PrintState, GcodeState, AMSFilamentSettings, NozzleType, IFilamentTray)

from PIL import Image


class Printer(IPrinter):
    """
    Client Class for connecting to the Bambulabs 3D printer
    """

    def __init__(self, ip_address: str, access_code: str, serial: str):
        """
        Initializes the printer interface with connection details.
        """
        pass

    def camera_client_alive(self) -> bool:
        """
        Check if the camera client is connected to the printer.
        Returns:
            bool: True if the camera loop is running.
        """
        pass

    def mqtt_client_connected(self) -> bool:
        """
        Get whether the MQTT client is connected to the printer.
        Returns:
            bool: True if the MQTT client is connected.
        """
        pass

    def mqtt_client_ready(self) -> bool:
        """
        Get whether the MQTT client is ready to send commands.
        Returns:
            bool: True if the MQTT client is ready.
        """
        pass

    def current_layer_num(self) -> int:
        """
        Get current layer number.
        Returns:
            int: Current layer number.
        """
        pass

    def total_layer_num(self) -> int:
        """
        Get total layer number.
        Returns:
            int: Total layer number.
        """
        pass

    def camera_start(self) -> bool:
        """
        Start the camera.
        Returns:
            bool: True if the camera successfully connected.
        """
        pass

    def mqtt_start(self) -> Any:  # The original returns MQTTErrorCode
        """
        Start the MQTT client.
        Returns:
            Any: Error code of loop start (or True for success if no specific error code object).
        """
        pass

    def mqtt_stop(self) -> None:
        """
        Stop the MQTT client.
        """
        pass

    def camera_stop(self) -> None:
        """
        Stop the camera client.
        """
        pass

    def connect(self) -> None:
        """
        Connect to the printer.
        """
        pass

    def disconnect(self) -> None:
        """
        Disconnect from the printer.
        """
        pass

    def get_time(self) -> Union[int, str, None]:
        """
        Get the remaining time of the print job in seconds.
        Returns:
            Union[int, str, None]: Remaining time in seconds, "Unknown", or None.
        """
        pass

    def mqtt_dump(self) -> dict[Any, Any]:
        """
        Get the MQTT dump of the messages recorded from the printer.
        Returns:
            dict[Any, Any]: The JSON recorded from the printer.
        """
        pass

    def get_percentage(self) -> Union[int, str, None]:
        """
        Get the percentage of the print job completed.
        Returns:
            Union[int, str, None]: Percentage completed, "Unknown", or None.
        """
        pass

    def get_state(self) -> GcodeState:
        """
        Get the state of the printer.
        Returns:
            GcodeState: The state of the printer.
        """
        pass

    def get_print_speed(self) -> int:
        """
        Get the print speed of the printer.
        Returns:
            int: The print speed of the printer.
        """
        pass

    def get_bed_temperature(self) -> Optional[float]:
        """
        Get the bed temperature of the printer.
        Returns:
            Optional[float]: The bed temperature or None if not printing.
        """
        pass

    def get_nozzle_temperature(self) -> Optional[float]:
        """
        Get the nozzle temperature of the printer.
        Returns:
            Optional[float]: The nozzle temperature or None if not printing.
        """
        pass

    def get_chamber_temperature(self) -> Optional[float]:
        """
        Get the chamber temperature of the printer.
        Returns:
            Optional[float]: The chamber temperature or None if not printing.
        """
        pass

    def nozzle_type(self) -> NozzleType:
        """
        Get the nozzle type currently registered to printer.
        Returns:
            NozzleType: Nozzle diameter.
        """
        pass

    def nozzle_diameter(self) -> float:
        """
        Get the nozzle diameter currently registered to printer.
        Returns:
            float: Nozzle diameter.
        """
        pass

    def get_file_name(self) -> str:
        """
        Get the name of the file being printed.
        Returns:
            str: The name of the file being printed.
        """
        pass

    def get_light_state(self) -> str:
        """
        Get the state of the printer light.
        Returns:
            str: The state of the printer light.
        """
        pass

    def turn_light_on(self) -> bool:
        """
        Turn on the printer light.
        Returns:
            bool: True if the light is turned on successfully.
        """
        pass

    def turn_light_off(self) -> bool:
        """
        Turn off the printer light.
        Returns:
            bool: True if the light is turned off successfully.
        """
        pass

    def gcode(self, gcode: Union[str, List[str]], gcode_check: bool = True) -> bool:
        """
        Send a G-code command to the printer.
        Parameters:
            gcode (Union[str, List[str]]): The G-code command or list of G-code commands.
            gcode_check (bool): Whether to check G-code validity. Defaults to True.
        Returns:
            bool: True if the G-code command is sent successfully.
        Raises:
            ValueError: If the G-code command is invalid.
        """
        pass

    def upload_file(self, file: BinaryIO, filename: str = "ftp_upload.gcode") -> str:
        """
        Upload a file to the printer.
        Parameters:
            file (BinaryIO): The file to be uploaded.
            filename (str, optional): The name of the file. Defaults to "ftp_upload.gcode".
        Returns:
            str: The path of the uploaded file.
        """
        pass

    def start_print(self,
                    filename: str,
                    plate_number: Union[int, str],
                    use_ams: bool = True,
                    ams_mapping: List[int] = None, # Changed default to None, will be [0] in implementation
                    skip_objects: Optional[List[int]] = None,
                    flow_calibration: bool = True) -> bool:
        """
        Start printing a file.
        Parameters:
            filename (str): The name of the file to be printed.
            plate_number (Union[int, str]): The plate number or path as a string.
            use_ams (bool, optional): Whether to use the AMS system. Defaults to True.
            ams_mapping (List[int], optional): The mapping of filament trays to plate numbers. Defaults to [0].
            skip_objects (Optional[List[int]]): List of G-code objects to skip. Defaults to None.
            flow_calibration (bool, optional): Whether to use automatic flow calibration. Defaults to True.
        Returns:
            bool: True if the file is printed successfully.
        """
        pass

    def stop_print(self) -> bool:
        """
        Stop the printer from printing.
        Returns:
            bool: True if the printer is stopped successfully.
        """
        pass

    def pause_print(self) -> bool:
        """
        Pause the printer from printing.
        Returns:
            bool: True if the printer is paused successfully.
        """
        pass

    def resume_print(self) -> bool:
        """
        Resume the printer from printing.
        Returns:
            bool: True if the printer is resumed successfully.
        """
        pass

    def set_bed_temperature(self, temperature: int) -> bool:
        """
        Set the bed temperature of the printer.
        Parameters:
            temperature (int): The temperature to be set.
        Returns:
            bool: True if the temperature is set successfully.
        """
        pass

    def home_printer(self) -> bool:
        """
        Home the printer.
        Returns:
            bool: True if the printer is homed successfully.
        """
        pass

    def move_z_axis(self, height: int) -> bool:
        """
        Move the Z-axis of the printer.
        Parameters:
            height (int): The height for the bed.
        Returns:
            bool: True if the Z-axis is moved successfully.
        """
        pass

    def set_filament_printer(self,
                             color: str,
                             filament: Union[str, AMSFilamentSettings],
                             ams_id: int = 255,
                             tray_id: int = 254) -> bool:
        """
        Set the filament of the printer.
        Parameters:
            color (str): The color of the filament (6-character hex code).
            filament (Union[str, AMSFilamentSettings]): The filament to be set.
            ams_id (int, optional): The index of the AMS. Defaults to 255 (external spool).
            tray_id (int, optional): The index of the spool/tray in the AMS. Defaults to 254 (external spool).
        Returns:
            bool: True if the filament is set successfully.
        """
        pass

    def set_nozzle_temperature(self, temperature: int) -> bool:
        """
        Set the nozzle temperature of the printer.
        Parameters:
            temperature (int): The temperature to be set.
        Returns:
            bool: True if the temperature is set successfully.
        """
        pass

    def set_print_speed(self, speed_lvl: int) -> bool:
        """
        Set the print speed of the printer.
        Parameters:
            speed_lvl (int): The speed level (0: Slowest, 1: Slow, 2: Fast, 3: Fastest).
        Returns:
            bool: True if the speed level is set successfully.
        """
        pass

    def delete_file(self, file_path: str) -> str:
        """
        Delete a file from the printer.
        Parameters:
            file_path (str): The path of the file to be deleted.
        Returns:
            str: The path of the deleted file.
        """
        pass

    def calibrate_printer(self,
                          bed_level: bool = True,
                          motor_noise_calibration: bool = True,
                          vibration_compensation: bool = True) -> bool:
        """
        Calibrate the printer.
        Parameters:
            bed_level (bool, optional): Whether to calibrate the bed level. Defaults to True.
            motor_noise_calibration (bool, optional): Whether to calibrate the motor noise. Defaults to True.
            vibration_compensation (bool, optional): Whether to calibrate the vibration compensation. Defaults to True.
        Returns:
            bool: True if the printer is calibrated successfully.
        """
        pass

    def load_filament_spool(self) -> bool:
        """
        Load the filament spool to the printer.
        Returns:
            bool: True if the filament spool is loaded successfully.
        """
        pass

    def unload_filament_spool(self) -> bool:
        """
        Unload the filament spool from the printer.
        Returns:
            bool: True if the filament spool is unloaded successfully.
        """
        pass

    def retry_filament_action(self) -> bool:
        """
        Retry the filament action.
        Returns:
            bool: True if the filament action is retried successfully.
        """
        pass

    def get_camera_frame(self) -> str:
        """
        Get the camera frame of the printer (base64 encoded).
        Returns:
            str: Base64 encoded image of the camera frame.
        """
        pass

    def get_camera_image(self) -> Image.Image:
        """
        Get the camera frame of the printer as a Pillow Image.
        Returns:
            Image.Image: Pillow Image of printer camera frame.
        """
        pass

    def get_current_state(self) -> PrintState:
        """
        Get the current state of the printer.
        Returns:
            PrintState: The current state of the printer.
        """
        pass

    def get_skipped_objects(self) -> List[int]:
        """
        Get the list of currently skipped objects.
        Returns:
            List[int]: A list of skipped object IDs.
        """
        pass

    def skip_objects(self, obj_list: List[int]) -> bool:
        """
        Skip Objects during printing.
        Args:
            obj_list (List[int]): object list to skip objects.
        Returns:
            bool: True if the publish command is successful.
        """
        pass

    def set_part_fan_speed(self, speed: Union[int, float]) -> bool:
        """
        Set the fan speed of the part fan.
        Args:
            speed (Union[int, float]): The speed to set the part fan.
        Returns:
            bool: True if setting the fan speed was successful.
        """
        pass

    def set_aux_fan_speed(self, speed: Union[int, float]) -> bool:
        """
        Set the fan speed of the auxiliary part fan.
        Args:
            speed (Union[int, float]): The speed to set the auxiliary part fan.
        Returns:
            bool: True if setting the fan speed was successful.
        """
        pass

    def set_chamber_fan_speed(self, speed: Union[int, float]) -> bool:
        """
        Set the fan speed of the chamber fan.
        Args:
            speed (Union[int, float]): The speed to set the chamber fan.
        Returns:
            bool: True if setting the fan speed was successful.
        """
        pass

    def set_auto_step_recovery(self, auto_step_recovery: bool = True) -> bool:
        """
        Set whether or not to set auto step recovery.
        Args:
            auto_step_recovery (bool): Flag to set auto step recovery. Defaults to True.
        Returns:
            bool: True if the auto step recovery command was successful.
        """
        pass

    def vt_tray(self) -> IFilamentTray:
        """
        Get the filament information from the tray information.
        Returns:
            IFilamentTray: Filament information.
        """
        pass

    def ams_hub(self) -> IAMSHub:
        """
        Get AMS hub, all AMS's hooked up to printer.
        Returns:
            IAMSHub: AMS information.
        """
        pass

    def subtask_name(self) -> str:
        """
        Get current subtask name (current print details).
        Returns:
            str: Current subtask name.
        """
        pass

    def gcode_file(self) -> str:
        """
        Get current G-code file (current print details).
        Returns:
            str: Current G-code file name.
        """
        pass

    def print_error_code(self) -> int:
        """
        Get current print error code.
        Returns:
            int: Error code (0 if normal).
        """
        pass

    def print_type(self) -> str:
        """
        Get what type of print the current printing file is from (cloud, local).
        Returns:
            str: Print type.
        """
        pass

    def wifi_signal(self) -> str:
        """
        Get Wifi signal in dBm.
        Returns:
            str: Wifi signal.
        """
        pass
