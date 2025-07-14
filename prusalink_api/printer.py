__all__ = ['Printer']

import base64
from io import BytesIO
from typing import Any, BinaryIO, Union, List, Optional
from PIL import Image
import requests
import json

from dorable_3dprinter_api import (
    IPrinter, PrintState, GcodeState, AMSFilamentSettings, NozzleType, IFilamentTray)

# Assuming IAMSHub is defined elsewhere if needed, otherwise it will remain abstract.
# For PrusaLink, AMS is not a concept, so IAMSHub methods will remain as pass.


class PrusaLinkPrinter(IPrinter):
    """
    Concrete implementation of the IPrinter interface for PrusaLink 3D printers.
    This class directly handles HTTP requests to the PrusaLink API.
    """

    def __init__(self, ip_address: str, access_code: str, serial: str, port: int = 80):
        """
        Initializes the PrusaLinkPrinter with connection details.

        Args:
            ip_address (str): The IP address of the PrusaLink printer.
            access_code (str): The API key for authentication with PrusaLink.
            serial (str): The serial number of the printer. (Stored but not used by PrusaLink API)
            port (int): The port number for the PrusaLink API. Defaults to 80.
        """
        self.ip_address = ip_address
        self.access_code = access_code
        self.serial = serial
        self.port = str(port) # Convert port to string for URL construction
        self.headers = {'X-Api-Key': access_code}
        self._last_status_data = None  # Cache for status data
        self._last_job_data = None     # Cache for job data
        self._last_info_data = None    # Cache for info data

    def _fetch_status_data(self) -> Optional[dict]:
        """Helper to fetch and cache printer status from /api/v1/status."""
        try:
            url = f'http://{self.ip_address}:{self.port}/api/v1/status'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            self._last_status_data = response.json()
            return self._last_status_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching status data from {url}: {e}")
            return None

    def _fetch_job_data(self) -> Optional[dict]:
        """Helper to fetch and cache job data from /api/v1/job."""
        try:
            url = f'http://{self.ip_address}:{self.port}/api/v1/job'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            # PrusaLink returns 204 No Content if no job is active
            if response.status_code == 204:
                self._last_job_data = None
            else:
                self._last_job_data = response.json()
            return self._last_job_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job data from {url}: {e}")
            return None

    def _fetch_info_data(self) -> Optional[dict]:
        """Helper to fetch and cache printer info from /api/v1/info."""
        try:
            url = f'http://{self.ip_address}:{self.port}/api/v1/info'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self._last_info_data = response.json()
            return self._last_info_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching info data from {url}: {e}")
            return None

    def camera_client_alive(self) -> bool:
        """
        Check if the camera client is connected to the printer.
        PrusaLink API does not expose this directly.
        """
        print("camera_client_alive: Not directly supported by PrusaLink API.")
        return False

    def mqtt_client_connected(self) -> bool:
        """
        Get whether the MQTT client is connected to the printer.
        PrusaLink uses HTTP, not MQTT.
        """
        print("mqtt_client_connected: Not applicable for PrusaLink (uses HTTP).")
        return False

    def mqtt_client_ready(self) -> bool:
        """
        Get whether the MQTT client is ready to send commands.
        PrusaLink uses HTTP, not MQTT.
        """
        print("mqtt_client_ready: Not applicable for PrusaLink (uses HTTP).")
        return False

    def current_layer_num(self) -> int:
        """
        Get current layer number.
        PrusaLink API provides print progress but not current layer number directly.
        """
        print("current_layer_num: Not directly supported by PrusaLink API.")
        return 0

    def total_layer_num(self) -> int:
        """
        Get total layer number.
        PrusaLink API provides print progress but not total layer number directly.
        """
        print("total_layer_num: Not directly supported by PrusaLink API.")
        return 0

    def camera_start(self) -> bool:
        """
        Start the camera.
        PrusaLink API does not expose a direct "start camera" command.
        Camera streams are typically accessed via specific endpoints.
        """
        print("camera_start: Not directly supported by PrusaLink API as a command.")
        return False

    def mqtt_start(self) -> Any:
        """
        Start the MQTT client.
        PrusaLink uses HTTP, not MQTT.
        """
        print("mqtt_start: Not applicable for PrusaLink (uses HTTP).")
        return False

    def mqtt_stop(self) -> None:
        """
        Stop the MQTT client.
        PrusaLink uses HTTP, not MQTT.
        """
        print("mqtt_stop: Not applicable for PrusaLink (uses HTTP).")
        pass

    def camera_stop(self) -> None:
        """
        Stop the camera client.
        PrusaLink API does not expose a direct "stop camera" command.
        """
        print("camera_stop: Not directly supported by PrusaLink API as a command.")
        pass

    def connect(self) -> None:
        """
        Connect to the printer.
        The connection is established implicitly by making HTTP requests.
        No explicit connect method is needed for HTTP.
        """
        print("connect: Connection is implicit via HTTP requests.")
        pass

    def disconnect(self) -> None:
        """
        Disconnect from the printer.
        No explicit disconnect method is needed for HTTP.
        """
        print("disconnect: Disconnection is implicit for HTTP requests.")
        pass

    def get_time(self) -> Union[int, str, None]:
        """
        Get the remaining time of the print job in seconds.
        """
        status_data = self._fetch_status_data()
        if status_data and 'job' in status_data and status_data['job']:
            return status_data['job'].get('time_remaining')
        return None

    def mqtt_dump(self) -> dict[Any, Any]:
        """
        Get the MQTT dump of the messages recorded from the printer.
        PrusaLink uses HTTP, not MQTT.
        """
        print("mqtt_dump: Not applicable for PrusaLink (uses HTTP).")
        return {}

    def get_percentage(self) -> Union[int, str, None]:
        """
        Get the percentage of the print job completed.
        """
        status_data = self._fetch_status_data()
        if status_data and 'job' in status_data and status_data['job']:
            # PrusaLink progress is a float, convert to int for percentage
            progress = status_data['job'].get('progress')
            if progress is not None:
                return int(progress)
        return None

    def get_state(self) -> GcodeState:
        """
        Get the state of the printer.
        Maps PrusaLink printer states to GcodeState enum.
        """
        status_data = self._fetch_status_data()
        if status_data and 'printer' in status_data:
            state = status_data['printer'].get('state')
            if state:
                # Map PrusaLink states to GcodeState
                if state == "PRINTING":
                    return GcodeState.RUNNING
                elif state == "PAUSED":
                    return GcodeState.PAUSE
                elif state == "FINISHED":
                    return GcodeState.FINISH
                elif state == "STOPPED":
                    # Assuming stopped is a form of failure for GcodeState based on provided enum
                    return GcodeState.FAILED
                elif state == "IDLE":
                    return GcodeState.IDLE
                elif state in ["BUSY", "ATTENTION", "READY"]:
                    # These states might precede a print, so mapping to PREPARE
                    return GcodeState.PREPARE
                elif state == "ERROR":
                    return GcodeState.FAILED
        return GcodeState.UNKNOWN

    def get_print_speed(self) -> int:
        """
        Get the print speed of the printer.
        """
        status_data = self._fetch_status_data()
        if status_data and 'printer' in status_data:
            speed = status_data['printer'].get('speed')
            if speed is not None:
                return int(speed)
        return 0

    def get_bed_temperature(self) -> Optional[float]:
        """
        Get the bed temperature of the printer.
        """
        status_data = self._fetch_status_data()
        if status_data and 'printer' in status_data:
            return status_data['printer'].get('temp_bed')
        return None

    def get_nozzle_temperature(self) -> Optional[float]:
        """
        Get the nozzle temperature of the printer.
        """
        status_data = self._fetch_status_data()
        if status_data and 'printer' in status_data:
            return status_data['printer'].get('temp_nozzle')
        return None

    def get_chamber_temperature(self) -> Optional[float]:
        """
        Get the chamber temperature of the printer.
        PrusaLink API does not expose chamber temperature.
        """
        print("get_chamber_temperature: Not supported by PrusaLink API.")
        return None

    def nozzle_type(self) -> NozzleType:
        """
        Get the nozzle type currently registered to printer.
        PrusaLink API provides nozzle diameter but not type (e.g., Stainless Steel, Hardened Steel).
        """
        print("nozzle_type: Not directly supported by PrusaLink API.")
        # Return a default or UNKNOWN if available in NozzleType
        return NozzleType.STAINLESS_STEEL # Defaulting as an example

    def nozzle_diameter(self) -> float:
        """
        Get the nozzle diameter currently registered to printer.
        """
        info_data = self._fetch_info_data()
        if info_data:
            diameter = info_data.get('nozzle_diameter')
            if diameter is not None:
                return float(diameter)
        return 0.0

    def get_file_name(self) -> str:
        """
        Get the name of the file being printed.
        """
        job_data = self._fetch_job_data()
        if job_data and 'file' in job_data and job_data['file']:
            return job_data['file'].get('display_name', job_data['file'].get('name', ''))
        return ""

    def get_light_state(self) -> str:
        """
        Get the state of the printer light.
        PrusaLink API does not expose printer light control.
        """
        print("get_light_state: Not supported by PrusaLink API.")
        return "Unknown"

    def turn_light_on(self) -> bool:
        """
        Turn on the printer light.
        PrusaLink API does not expose printer light control.
        """
        print("turn_light_on: Not supported by PrusaLink API.")
        return False

    def turn_light_off(self) -> bool:
        """
        Turn off the printer light.
        PrusaLink API does not expose printer light control.
        """
        print("turn_light_off: Not supported by PrusaLink API.")
        return False

    def gcode(self, gcode: Union[str, List[str]], gcode_check: bool = True) -> bool:
        """
        Send a G-code command to the printer.
        PrusaLink API does not support sending arbitrary G-code commands directly.
        It primarily works with G-code files.
        """
        print("gcode: Not directly supported by PrusaLink API (file-based printing).")
        return False

    def upload_file(self, file: BinaryIO, filename: str = "ftp_upload.gcode") -> str:
        """
        Upload a file to the printer.
        """
        try:
            file_content = file.read()
            url = f'http://{self.ip_address}:{self.port}/api/v1/files/usb/{filename}'
            
            # Create a copy of headers to add specific headers for this request
            request_headers = self.headers.copy()
            request_headers['Content-Length'] = str(len(file_content))
            request_headers['Content-Type'] = 'application/octet-stream'

            response = requests.put(url, headers=request_headers, data=file_content)
            response.raise_for_status()
            
            if response.status_code == 201: # 201 Created on success
                return f"/usb/{filename}" # Return the remote path
            else:
                print(f"File upload failed with status code: {response.status_code}")
                return ""
        except requests.exceptions.RequestException as e:
            print(f"Error uploading file: {e}")
            return ""

    def start_print(self,
                    filename: str,
                    plate_number: Union[int, str], # Not directly applicable to PrusaLink
                    use_ams: bool = True, # Not applicable to PrusaLink
                    ams_mapping: List[int] = None, # Not applicable to PrusaLink
                    skip_objects: Optional[List[int]] = None, # Not applicable to PrusaLink
                    flow_calibration: bool = True) -> bool: # Not applicable to PrusaLink
        """
        Start printing a file.
        For PrusaLink, this means starting a print job from an already uploaded file.
        The `filename` parameter should be the full path on the printer, e.g., '/usb/my_print.gcode'.
        Other parameters (plate_number, use_ams, ams_mapping, skip_objects, flow_calibration) are ignored.
        """
        try:
            # The OpenAPI spec for POST /api/v1/files/{storage}/{path} indicates
            # that the body is ignored and it starts the print.
            url = f'http://{self.ip_address}:{self.port}/api/v1/files/usb{filename}'
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return response.status_code == 204 # 204 No Content for success
        except requests.exceptions.RequestException as e:
            print(f"Error starting print: {e}")
            return False

    def stop_print(self) -> bool:
        """
        Stop the printer from printing.
        Requires fetching the current job ID first.
        """
        job_data = self._fetch_job_data()
        if job_data and 'id' in job_data:
            job_id = str(job_data['id'])
            try:
                url = f'http://{self.ip_address}:{self.port}/api/v1/job/{job_id}'
                response = requests.delete(url, headers=self.headers)
                response.raise_for_status()
                return response.status_code == 204 # 204 No Content for success
            except requests.exceptions.RequestException as e:
                print(f"Error stopping print for job ID {job_id}: {e}")
                return False
        print("No active job to stop.")
        return False

    def pause_print(self) -> bool:
        """
        Pause the printer from printing.
        Requires fetching the current job ID first.
        """
        job_data = self._fetch_job_data()
        if job_data and 'id' in job_data:
            job_id = str(job_data['id'])
            try:
                url = f'http://{self.ip_address}:{self.port}/api/v1/job/{job_id}/pause'
                response = requests.put(url, headers=self.headers)
                response.raise_for_status()
                return response.status_code == 204 # 204 No Content for success
            except requests.exceptions.RequestException as e:
                print(f"Error pausing print for job ID {job_id}: {e}")
                return False
        print("No active job to pause.")
        return False

    def resume_print(self) -> bool:
        """
        Resume the printer from printing.
        Requires fetching the current job ID first.
        """
        job_data = self._fetch_job_data()
        if job_data and 'id' in job_data:
            job_id = str(job_data['id'])
            try:
                url = f'http://{self.ip_address}:{self.port}/api/v1/job/{job_id}/resume'
                response = requests.put(url, headers=self.headers)
                response.raise_for_status()
                return response.status_code == 204 # 204 No Content for success
            except requests.exceptions.RequestException as e:
                print(f"Error resuming print for job ID {job_id}: {e}")
                return False
        print("No active job to resume.")
        return False

    def set_bed_temperature(self, temperature: int) -> bool:
        """
        Set the bed temperature of the printer.
        PrusaLink API does not expose direct temperature setting commands.
        This is usually done via G-code in the print file.
        """
        print("set_bed_temperature: Not directly supported by PrusaLink API.")
        return False

    def home_printer(self) -> bool:
        """
        Home the printer.
        PrusaLink API does not expose direct homing commands.
        This is usually done via G-code.
        """
        print("home_printer: Not directly supported by PrusaLink API.")
        return False

    def move_z_axis(self, height: int) -> bool:
        """
        Move the Z-axis of the printer.
        PrusaLink API does not expose direct axis movement commands.
        This is usually done via G-code.
        """
        print("move_z_axis: Not directly supported by PrusaLink API.")
        return False

    def set_filament_printer(self,
                             color: str,
                             filament: Union[str, AMSFilamentSettings],
                             ams_id: int = 255,
                             tray_id: int = 254) -> bool:
        """
        Set the filament of the printer.
        PrusaLink does not have an AMS system or direct filament setting commands.
        """
        print("set_filament_printer: Not applicable for PrusaLink (no AMS/direct filament control).")
        return False

    def set_nozzle_temperature(self, temperature: int) -> bool:
        """
        Set the nozzle temperature of the printer.
        PrusaLink API does not expose direct temperature setting commands.
        This is usually done via G-code in the print file.
        """
        print("set_nozzle_temperature: Not directly supported by PrusaLink API.")
        return False

    def set_print_speed(self, speed_lvl: int) -> bool:
        """
        Set the print speed of the printer.
        PrusaLink API provides current speed but not direct setting of speed level.
        This is usually done via G-code or printer controls.
        """
        print("set_print_speed: Not directly supported by PrusaLink API.")
        return False

    def delete_file(self, file_path: str) -> str:
        """
        Delete a file from the printer.
        The `file_path` should be the full path on the printer, e.g., '/usb/my_file.gcode'.
        """
        try:
            url = f'http://{self.ip_address}:{self.port}/api/v1/files/usb{file_path}'
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            if response.status_code == 204: # 204 No Content for success
                return file_path
            else:
                print(f"File deletion failed with status code: {response.status_code}")
                return ""
        except requests.exceptions.RequestException as e:
            print(f"Error deleting file: {e}")
            return ""

    def calibrate_printer(self,
                          bed_level: bool = True,
                          motor_noise_calibration: bool = True,
                          vibration_compensation: bool = True) -> bool:
        """
        Calibrate the printer.
        PrusaLink API does not expose direct calibration commands.
        """
        print("calibrate_printer: Not directly supported by PrusaLink API.")
        return False

    def load_filament_spool(self) -> bool:
        """
        Load the filament spool to the printer.
        PrusaLink API does not expose direct filament loading/unloading commands.
        """
        print("load_filament_spool: Not directly supported by PrusaLink API.")
        return False

    def unload_filament_spool(self) -> bool:
        """
        Unload the filament spool from the printer.
        PrusaLink API does not expose direct filament loading/unloading commands.
        """
        print("unload_filament_spool: Not directly supported by PrusaLink API.")
        return False

    def retry_filament_action(self) -> bool:
        """
        Retry the filament action.
        PrusaLink API does not expose direct filament action retry commands.
        """
        print("retry_filament_action: Not directly supported by PrusaLink API.")
        return False

    def get_camera_frame(self) -> str:
        """
        Get the camera frame of the printer (base64 encoded).
        """
        try:
            # Attempt to get snapshot from default camera
            url = f'http://{self.ip_address}:{self.port}/api/v1/cameras/snap'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if response.status_code == 200 and 'image/png' in response.headers.get('Content-Type', ''):
                return base64.b64encode(response.content).decode('utf-8')
            else:
                print(f"Failed to get camera frame. Status: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
                return ""
        except requests.exceptions.RequestException as e:
            print(f"Error getting camera frame from {url}: {e}")
            return ""

    def get_camera_image(self) -> Image.Image:
        """
        Get the camera frame of the printer as a Pillow Image.
        """
        base64_frame = self.get_camera_frame()
        if base64_frame:
            try:
                image_bytes = base64.b64decode(base64_frame)
                return Image.open(BytesIO(image_bytes))
            except Exception as e:
                print(f"Error decoding or opening image: {e}")
                raise
        raise ValueError("No camera frame available or failed to retrieve.")

    def get_current_state(self) -> PrintState:
        """
        Get the current state of the printer.
        Maps PrusaLink printer states to PrintState enum.
        This mapping is approximate as PrusaLink states are high-level.
        """
        status_data = self._fetch_status_data()
        if status_data and 'printer' in status_data:
            state = status_data['printer'].get('state')
            if state:
                if state == "PRINTING":
                    return PrintState.PRINTING
                elif state == "PAUSED":
                    # PrusaLink doesn't provide specific pause reasons
                    return PrintState.PAUSED_USER
                elif state == "FINISHED":
                    return PrintState.IDLE # Finished state can be considered IDLE after job completion
                elif state == "STOPPED":
                    return PrintState.IDLE # Stopped state can be considered IDLE after job termination
                elif state == "ERROR":
                    return PrintState.UNKNOWN # Or a more specific error state if available in PrintState
                elif state == "IDLE":
                    return PrintState.IDLE
                elif state == "BUSY":
                    return PrintState.UNKNOWN # Busy could mean various things, mapping to UNKNOWN
                elif state == "ATTENTION":
                    return PrintState.UNKNOWN # Attention could mean various things, mapping to UNKNOWN
                elif state == "READY":
                    return PrintState.IDLE # Ready is similar to idle for starting new jobs
        return PrintState.UNKNOWN

    def get_skipped_objects(self) -> List[int]:
        """
        Get the list of currently skipped objects.
        PrusaLink API does not support skipping objects.
        """
        print("get_skipped_objects: Not supported by PrusaLink API.")
        return []

    def skip_objects(self, obj_list: List[int]) -> bool:
        """
        Skip Objects during printing.
        PrusaLink API does not support skipping objects.
        """
        print("skip_objects: Not supported by PrusaLink API.")
        return False

    def set_part_fan_speed(self, speed: Union[int, float]) -> bool:
        """
        Set the fan speed of the part fan.
        PrusaLink API does not expose direct fan speed control.
        """
        print("set_part_fan_speed: Not supported by PrusaLink API.")
        return False

    def set_aux_fan_speed(self, speed: Union[int, float]) -> bool:
        """
        Set the fan speed of the auxiliary part fan.
        PrusaLink API does not expose direct fan speed control.
        """
        print("set_aux_fan_speed: Not supported by PrusaLink API.")
        return False

    def set_chamber_fan_speed(self, speed: Union[int, float]) -> bool:
        """
        Set the fan speed of the chamber fan.
        PrusaLink API does not expose direct fan speed control.
        """
        print("set_chamber_fan_speed: Not supported by PrusaLink API.")
        return False

    def set_auto_step_recovery(self, auto_step_recovery: bool = True) -> bool:
        """
        Set whether or not to set auto step recovery.
        PrusaLink API does not expose this setting.
        """
        print("set_auto_step_recovery: Not supported by PrusaLink API.")
        return False

    def vt_tray(self) -> IFilamentTray:
        """
        Get the filament information from the tray information.
        PrusaLink does not have a concept of 'trays' like Bambu Lab's AMS.
        """
        print("vt_tray: Not applicable for PrusaLink (no AMS/trays).")
        raise NotImplementedError("Filament tray information not available for PrusaLink.")

    def ams_hub(self) -> Any: # Changed return type to Any as IAMSHub is not defined in context
        """
        Get AMS hub, all AMS's hooked up to printer.
        PrusaLink does not have an AMS system.
        """
        print("ams_hub: Not applicable for PrusaLink (no AMS).")
        raise NotImplementedError("AMS hub information not available for PrusaLink.")

    def subtask_name(self) -> str:
        """
        Get current subtask name (current print details).
        PrusaLink API does not expose a subtask name.
        """
        print("subtask_name: Not directly supported by PrusaLink API.")
        return ""

    def gcode_file(self) -> str:
        """
        Get current G-code file (current print details).
        This is the same as get_file_name for PrusaLink.
        """
        return self.get_file_name()

    def print_error_code(self) -> int:
        """
        Get current print error code.
        PrusaLink API provides error messages but not specific integer error codes for print status.
        The `Error` schema is for API response errors, not ongoing print errors.
        """
        print("print_error_code: Not directly supported by PrusaLink API.")
        return 0 # 0 for no error

    def print_type(self) -> str:
        """
        Get what type of print the current printing file is from (cloud, local).
        PrusaLink API does not explicitly provide the origin of the print file.
        """
        print("print_type: Not directly supported by PrusaLink API.")
        return "Unknown"

    def wifi_signal(self) -> str:
        """
        Get Wifi signal in dBm.
        PrusaLink API does not expose WiFi signal strength.
        """
        print("wifi_signal: Not supported by PrusaLink API.")
        return "Unknown"

