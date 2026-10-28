import os
import tkinter as tk
import xml.etree.ElementTree as ET
from lxml import etree
from pywintypes import com_error
from win32com.client import Dispatch
from tkinter import messagebox, filedialog

class ControlDeskHandler():
    def __init__(self):
        try:
            self.application = Dispatch("ControlDeskNG.Application")
            self.main_platform = self.find_main_platform()
            self.experiment_directoy = os.path.dirname(self.application.ActiveExperiment.DirectoryName)
            self.experiment_source = os.path.dirname(self.main_platform.ActiveVariableDescription.SourceFullName)
            self.hil_name = self.application.ActiveExperiment.Name
            self.source_directory = self.experiment_directoy + '\\' + self.experiment_source
            self.control_desk_version = self.application.Version
            self.online_calibration_state = self.application.CalibrationManagement.State
            self.active_layout = None
            self.last_instrument = None
            self.sDefaultLayoutName = 'Automated Layout'
            self.sDefaultIntrumentName = 'Automated Instrument'
            self.lDatasets = []
            self.sDatasetPath = ''
            self.sCreatedSdfPaths = ''
            self.lLayoutConnections = []
            self.connection_file_tree = None
            self.parent_map = None
            self.lLinesFormVariablePaths = []
            self.lConnecionsToBeCorrected = []
            self.loging_function = None
            self.sdf_file = ''
        except Exception as error:
            print(error)
            return None
        try:
            for file in os.listdir(self.source_directory):
                if file.endswith('sdf_paths.txt'):
                    self.sdf_file = os.path.normpath(f'{self.source_directory}\{file}')
                    break
        except Exception as error:
            print('Source Directory cannot be opened.')
            print(error)

    def find_main_platform(self):
        for platform in self.application.ActiveExperiment.Platforms:
            if platform.Type == 22:
                return platform
        return self.application.ActiveExperiment.Platforms[0]

    def find_active_layout(self, sLayoutName:str):
        self.active_layout = None
        for index, layout in enumerate(self.application.LayoutManagement.Layouts):
                if layout.Name == sLayoutName:
                    self.active_layout = self.application.LayoutManagement.Layouts.Item(index)
                    return self.active_layout
        try:
            self.active_layout = self.application.LayoutManagement.Layouts.Add(sLayoutName)
        except com_error as error:
            window = tk.Tk()
            window.withdraw()
            messagebox.showwarning('Layout Error', f'A Layout exists with the same name "{sLayoutName}"!.\nPlease delete this file form hard disk, then try again.')
        return self.active_layout

    def find_active_instrument(self, sInstrumentName:str, active_layout, position_x=0, position_y=0, width=500, height=400):
        for index, instrument in enumerate(active_layout.Instruments):
            if instrument.Name == sInstrumentName:
                self.last_instrument = active_layout.Instruments.Item(index)
                return self.last_instrument
        self.last_instrument = active_layout.Instruments.Add("Variable Array", sInstrumentName, position_x, position_y, width, height)
        return self.last_instrument

    def get_control_desk_instrument(self, sLayoutName:str = "Automated Layout", sInstrumentName:str = "Automated Instrument"):
        active_layout = self.find_active_layout(sLayoutName)
        if active_layout:
            position_y = 0
            if list(active_layout.Instruments):
                last_instrument = list(active_layout.Instruments)[-1]
                position_y = last_instrument.Position.Height + last_instrument.Position.Y
            return self.find_active_instrument(sInstrumentName, active_layout, position_y)
        else:
            return None

    def create_variable_arrays_from(self, sInputPath:str, sLayoutName:str = "Automated Layout", sInstrumentName:str = "Automated Instrument"):
        active_instrument = self.get_control_desk_instrument(sLayoutName, sInstrumentName)
        if active_instrument:
            for line in list(filter(None, sInputPath.split("\n"))):
                if not line.endswith("=>") and not "":  
                    sIdentifier = line.strip()
                    if not sIdentifier.startswith("Platform()://"):
                        sIdentifier = "Platform()://" + sIdentifier
                    if self.control_desk_version.startswith('2'):
                        variable = self.application.VariablesManagement.FindVariable(sIdentifier)
                        if variable.Type == 16:
                            lIdentifiers = [element.Identifier.Path for element in variable.SubElements]
                            for sIdentifier in lIdentifiers:
                                instrument_row = self.add_row_to_variable_array(sIdentifier=sIdentifier,
                                                                                variable_array_instrument=active_instrument)
                        else:
                            instrument_row = self.add_row_to_variable_array(sIdentifier=sIdentifier,
                                                                            variable_array_instrument=active_instrument)
            try:
                return instrument_row
            except UnboundLocalError:
                pass
        else:
            print('Error occured as creating control desk instrument!')

    def add_row_to_variable_array(self, sIdentifier, variable_array_instrument):
        tempRow = variable_array_instrument.Rows.Add()
        try:
            tempRow.MainVariable = sIdentifier
        except com_error:
            tempRow.UseCustomColor = True
            tempRow.BackgroundColor = 3026687
        return tempRow

    def add_column(self, sLayoutName:str, sInstrumentName:str, sColumnName:str=''):
        active_instrument = self.get_control_desk_instrument(sLayoutName, sInstrumentName)
        active_instrument.Column.Add()

    def delete_column(self, sLayoutName:str, sInstrumentName:str, sColumnName:str):
        for column in self.get_control_desk_instrument(sLayoutName, sInstrumentName).Columns:
            if column.Header.Text == sColumnName:
                column.Delete()

    def get_sdf_path(self):
        return self.sdf_file

    def get_dataset_directory(self):
        # print('Experiment Directory:', self.application.ActiveExperiment.DirectoryName)
        # self.sDatasetPath = self.application.ActiveExperiment.DirectoryName + '\Data Sets'
        return self.sDatasetPath

    def create_dataset_list(self):
        try:
            for platform in self.main_platform.Platforms:
                if platform.VariableDescriptions.Count > 0:
                    for dataset in platform.ActiveVariableDescription.DataSets:
                        if dataset:
                            self.lDatasets.append(dataset.FileName)
            if len(self.lDatasets) > 0:
                self.sDatasetPath = dataset.DirectoryName
        except com_error:
            print('Datasets könnten nicht über dem Control Desk geladen werden!')

    def load_datasets_in_active_project(self):
        try:
            for platform in self.main_platform.Platforms:
                for dataset in platform.ActiveVariableDescription.DataSets:
                    dataset.Close()
            for platform in self.main_platform.Platforms:
                for dataset in platform.ActiveVariableDescription.DataSets:
                    dataset.AutomaticDownloadEnabled
                    dataset.WriteToHardware()
        except com_error as error:
            window = tk.Tk()
            window.withdraw()
            messagebox.showwarning('Layout Error', f'Dataset {dataset.FileName} cannot be actived!\nIt should be open form Control Desk manually.')

    def select_variable(self, sVariableName:str):
        if sVariableName.startswith(' '):
            sVariableName = list(sVariableName[1:])
        if not sVariableName.startswith('Platform()://'):
            sVariableName = 'Platform()://' + sVariableName
        sVariableName = sVariableName.strip('\n')
        try:
            self.application.VariablesManagement.VariableBrowser.VariableView.SelectItems(sVariableName, sVariableName)
            return True
        except Exception as Error:
            print(Exception)
            return False

    def find_variable(self, sIdentifier:str):
        return self.application.VariablesManagement.FindVariable(sIdentifier)

    def find_variable_in_sdf(self, sIdentifier:str):
        sIdentifier = sIdentifier.replace('Platform()://', '')
        if len(self.lLinesFormVariablePaths) == 0 or sIdentifier not in self.lLinesFormVariablePaths:
            return None
        return sIdentifier

    def update_default_layout_name(self, sNewDefaultLayoutName: str):
        if len(sNewDefaultLayoutName) > 0:
            self.sDefaultLayoutName = sNewDefaultLayoutName

    def update_default_instrument_name(self, sNewDefaultInstrumentName: str):
        if len(sNewDefaultInstrumentName) > 0:
            self.sDefaultIntrumentName = sNewDefaultInstrumentName

    def create_sdf_paths_from_active_project(self):
        self.sCreatedSdfPaths = ''
        for platfrom in self.main_platform.Platforms:
            print(f'{platfrom.Name} is being searched for variable paths...')
            for var in platfrom.ActiveVariableDescription.Variables:
                # print(var.Identifier.Path)
                self.sCreatedSdfPaths += var.Identifier.Path + '\n'

    def save_created_sdf_paths(self):
        if len(self.sCreatedSdfPaths) > 0:
            sSdfPathToSave = filedialog.asksaveasfilename(title='Save Created SDF Variable Paths',
                                                        filetypes=[('Variable Paths SDF-File', '*.sdf_paths.txt')],
                                                        initialfile='HiL.sdf_paths.txt')
            with open(file=sSdfPathToSave, mode='w') as file_to_write:
                file_to_write.write(self.sCreatedSdfPaths)

    def open_all_layouts(self):
        for layout in self.application.LayoutManagement.Files:
            layout.Open()

    def read_HiLVariables(self, sPath:str=''):
        self.lLinesFormVariablePaths = []
        if len(sPath) == 0:
            sPath = self.sdf_file
        with open(sPath, mode='r') as path_file:
            for line in path_file.read().splitlines():
                if '/Signal Chain/I/O Function View/Communication/' in line:
                    line = line.replace('/Signal Chain/I/O Function View/Communication/', '/Signal Chain/IO Function View/Communication/')
                line = line.split('//')[-1]
                self.lLinesFormVariablePaths.append(line)

    def read_layout_connections(self, sXmlTempFilePath:str='', bWriteLog:bool=True):
        if len(sXmlTempFilePath) == 0: 
            sXmlTempFilePath = 'C:/Temp/HiL_Layout_Paths.conx'
        self.application.LayoutManagement.Layouts.ExportConnectionFile(sXmlTempFilePath)
        if os.path.exists(sXmlTempFilePath):
            # print(f'Layout file is found:\n{sXmlTempFilePath}\n')
            self.connection_file_tree = ET.parse(sXmlTempFilePath)
            root = self.connection_file_tree.getroot()
            self.parent_map = {child: parent for parent in root.iter() for child in parent}
            self.lLayoutConnections = list(root.iter(tag='Connection'))
            # print(f'{len(self.lLayoutConnections)} connections found in layout file.\n')
            if bWriteLog:
                self.write_log(f'{len(self.lLayoutConnections)} connections found in layout file.\n')

    def replace_path_in_connection(self, connection:ET.Element, sNewPath:str):
        if connection.get('Identifier').startswith('Platform()://'):
            sNewPath = 'Platform()://' + sNewPath
        connection.set('Identifier', sNewPath)

    def replace_instrument_main_variable(self, sLayoutName:str, sInstrumentName:str, sNewMainVariable:str,
                                         iRowNumber:int=0, iYAxisIndex:int=0, iSignalIndex:int=0, sPlotAxis=''):
        # print(f'{sLayoutName=}')
        # print(f'{sInstrumentName=}')
        # print(f'{sNewMainVariable=}')
        try:
            control_desk_layout = self.application.LayoutManagement.Layouts.Item(sLayoutName)
            control_desk_instrument = control_desk_layout.GetInstrument(sInstrumentName)
            sNewMainVariable = 'Platform()://' + sNewMainVariable
            if control_desk_instrument.TypeName == 'Variable Array':
                control_desk_instrument.Rows[iRowNumber].MainVariable = sNewMainVariable
            elif control_desk_instrument.TypeName == 'XY Plotter':
                if sPlotAxis == 'XVariable':
                    control_desk_instrument.Curves[iRowNumber].XVariable.Connection = sNewMainVariable
                elif sPlotAxis == 'YVariable':
                    control_desk_instrument.Curves[iRowNumber].YVariable.Connection = sNewMainVariable
            elif control_desk_instrument.TypeName == 'Time Plotter':
                control_desk_instrument.Plots[iRowNumber].YAxes[iYAxisIndex].Signals[iSignalIndex].Connection = sNewMainVariable
            else:
                control_desk_instrument.MainVariable = sNewMainVariable
        except Exception as error:
            print(f'\n{sInstrumentName} cannot be repaired. Reason:\n{error}')
            print(f'Layout Name: {sLayoutName}\nInstrument Name: {sInstrumentName}\nRow Number: {iRowNumber}\nCorrected Path: {sNewMainVariable}')
            self.write_log(f'\n{sInstrumentName} cannot be repaired. Reason:\n{error}')

    def save_layout_connections(self, sNewXmlConnectionFilePath:str=''):
        if not self.connection_file_tree:
            return
        if len(sNewXmlConnectionFilePath) == 0:
            sNewXmlConnectionFilePath = 'C:/Temp/Modified_HiL_Layout_Paths.conx'
        self.connection_file_tree.write(sNewXmlConnectionFilePath, encoding='utf-8', xml_declaration=True)

    def import_layout_connections(self, sModifiedConnectionFilePath:str=''):
        if len(sModifiedConnectionFilePath) == 0:
            sModifiedConnectionFilePath = 'C:/Temp/Modified_HiL_Layout_Paths.conx'
        self.application.LayoutManagement.Layouts.ImportConnectionFile(sModifiedConnectionFilePath)

    def find_faulty_connection_paths(self):
        if len(self.lLayoutConnections) == 0 or len(self.lLinesFormVariablePaths) == 0:
            return
        self.lConnecionsToBeCorrected = []
        for connection in self.lLayoutConnections:
            sMainVariable = connection.get('Identifier')
            if self.control_desk_version.startswith('2'):
                sFoundPath = self.find_variable(sIdentifier=sMainVariable)
            else:
                sFoundPath = self.find_variable_in_sdf(sIdentifier=sMainVariable)
            if not sFoundPath:
                control_desk_instrument = self.parent_map.get(connection)
                control_desk_layout = self.parent_map.get(control_desk_instrument)
                sLayoutName = control_desk_layout.get('Name')
                sInstrumentName = control_desk_instrument.get('Name')
                sAxis = ''
                iYAxisIndex = 0
                iSignalIndex = 0
                if control_desk_instrument.get('Type') == "Variable Array":
                    iRowNumber = parse_decimal_string_to_int(connection.get('Key').strip("'").strip('Row'))
                elif control_desk_instrument.get('Type') == 'XY Plotter':
                    iRowNumber = parse_decimal_string_to_int(connection.get('Key').strip("'Curve").split("'")[0])
                    sAxis = connection.get('Key').strip("Curve").split("'")[2]
                elif control_desk_instrument.get('Type') == 'Time Plotter':
                    iRowNumber = parse_decimal_string_to_int(connection.get('Key').replace("Plot", "").split("'")[1])
                    iYAxisIndex = parse_decimal_string_to_int(connection.get('Key').replace("YAxis", "").split("'")[2])
                    iSignalIndex = parse_decimal_string_to_int(connection.get('Key').replace("Signal", "").split("'")[3])
                else:
                    iRowNumber = 0
                self.lConnecionsToBeCorrected.append({'Layout Name': sLayoutName,
                                                      'Instrument Name': sInstrumentName,
                                                      'Row Number': iRowNumber,
                                                      'Y Axis Index': iYAxisIndex,
                                                      'Signal Index': iSignalIndex,
                                                      'Plot Axis' : sAxis,
                                                      'Main Variable': sMainVariable})
        self.write_log(f'{len(self.lConnecionsToBeCorrected)} faulty paths found in layout connections')

    def search_path_in_sdf_variables(self, sSeachedPath:str) -> list:
        if len(self.lLinesFormVariablePaths) == 0 or len(sSeachedPath) == 0:
            return []
        iVariableArrayIndex = None
        if sSeachedPath.endswith(']'):
            iVariableArrayIndex = parse_decimal_string_to_int(sSeachedPath[-2])
            sSeachedPath = sSeachedPath[:-3]
        lTempPath = sSeachedPath.split('//')[-1].split('/')
        sFullPath = "/".join(lTempPath[1:])
        lFoundPaths = []
        lCommon = []
        sRouterSignalName = ''
        sSearchString = ''
        sSearchString_2 = ''
        sExcludedString = ''
        if lTempPath[-3] == 'Signals':
            sTemp = lTempPath[-4]
            lTempPath[-4] = lTempPath[-3]
            lTempPath[-3] = sTemp
        sTempPath = sSeachedPath.replace("/ECU_Versorgung/", "/Klemmensteuerung/")
        if "/Klemmensteuerung/" in sTempPath:
            sSearchString = '/'.join(lTempPath[-3:])
        elif len(lTempPath) > 6:
            sSearchString = '/'.join(lTempPath[-4:])
        elif "_write_" in sTempPath or "_read_" in sTempPath:
            sSearchString = "BusRouter_" + '/'.join(lTempPath[1:4]).split("_XIX_")[1]
            sRouterSignalName = lTempPath[-1]
            sSearchString_2 = sRouterSignalName
            sExcludedString = sRouterSignalName + "_"
        elif "/Model Root/" in sTempPath:
            sSearchString = "/Model Root/" + sTempPath.split("/Model Root/")[-1]
        if "_Unterbrechung_no_RealECU" in sSearchString:
            sSearchString = sSearchString.replace("_no_RealECU","")
        if lTempPath[-2] != "Active" and lTempPath[-1] == "Active":
            sSearchString += "/Active"
        sSearchString = sSearchString.replace("Relais_EL", "Relais")
        if len(sSearchString) != 0:
            for sPath in self.lLinesFormVariablePaths:
                if not iVariableArrayIndex and sFullPath in sPath:
                    lFoundPaths = []
                    lFoundPaths.append(sPath)
                    break
                if len(sRouterSignalName) > 0:
                    if sSearchString in sPath and sRouterSignalName in sPath and not sExcludedString in sPath:
                        lFoundPaths.append(sPath)
                elif sSearchString in sPath:
                    lTraceKeywords = ["Ethernet", "Inspection", "Manipulation", "Simulated ECUs"]
                    lCommon = [sKeyword for sKeyword in lTraceKeywords if sKeyword in lTempPath]
                    if len(lCommon) != 0:
                        iTempIndex = lTempPath.index(lCommon[0])
                        if lCommon[0] == "Ethernet":
                            sSearchString_2 = lTempPath[iTempIndex - 1] + '/' + lCommon[0] + '/' + lTempPath[iTempIndex + 1] + '/'
                        elif lCommon[0] == "BusRouter":
                            sSearchString_2 = '/' + lCommon[0] + '/'
                        else:
                            lTempPath[iTempIndex - 1] = lTempPath[iTempIndex - 1].replace('_local','')
                            sBusName = lTempPath[iTempIndex - 1].replace('BusConfig_', '').replace('_Gateway', '')
                            sSearchString_2 = lTempPath[iTempIndex - 1] + '/' + lCommon[0] + '/' + sBusName + '/' + lTempPath[iTempIndex + 2] + '/'
                            # sSearchString_2 = lTempPath[iTempIndex - 1] + '/' + lCommon[0] + '/' + lTempPath[iTempIndex + 1] + '/' + lTempPath[iTempIndex + 2]
                        if sSearchString_2 not in sPath:
                            continue
                    if iVariableArrayIndex is not None:
                        sPath += f'[{iVariableArrayIndex}]'
                    lFoundPaths.append(sPath)
            if len(lFoundPaths) != 1:
                self.write_log(f'\nLayout Path: {sTempPath}\nSearch String 1: {sSearchString}\nSearch String 2: {sSearchString_2}\nExcluded String: {sExcludedString}\nFound Paths:')
                for line in lFoundPaths:
                    self.write_log(line)
        return lFoundPaths   

    def repair_faulty_connection_paths(self):
        self.application.LayoutManagement.KeepInvalidConnectionsDuringImport = False
        if len(self.lConnecionsToBeCorrected) == 0:
            return
        for connection in self.lConnecionsToBeCorrected:
            lFoundPaths = self.search_path_in_sdf_variables(connection.get('Identifier'))
            if len(lFoundPaths) == 1:
                self.replace_path_in_connection(connection, lFoundPaths[0])
        iOldFaultPathNumber = len(self.lConnecionsToBeCorrected)
        self.find_faulty_connection_paths() 
        self.write_log(f'{iOldFaultPathNumber} faulty paths are reduced to {len(self.lConnecionsToBeCorrected)}.')

    def repair_faulty_layout_main_variables(self):
        if len(self.lConnecionsToBeCorrected) == 0:
            return
        iOldFaultPathNumber = len(self.lConnecionsToBeCorrected)
        for connection in self.lConnecionsToBeCorrected:
            lFoundPaths = self.search_path_in_sdf_variables(connection['Main Variable'])
            if len(lFoundPaths) == 1:
                self.replace_instrument_main_variable(sLayoutName=connection['Layout Name'], 
                                                      sInstrumentName=connection['Instrument Name'], 
                                                      sNewMainVariable=lFoundPaths[0], 
                                                      iRowNumber=connection['Row Number'],
                                                      iYAxisIndex=connection['Y Axis Index'],
                                                      iSignalIndex=connection['Signal Index'],
                                                      sPlotAxis=connection['Plot Axis'])
        self.write_log('\n')
        self.read_layout_connections(bWriteLog=False)
        self.find_faulty_connection_paths() 
        self.write_log(f'{iOldFaultPathNumber} faulty paths have been reduced to {len(self.lConnecionsToBeCorrected)}.')

    def write_log(self, sLog:str=''):
        if not self.loging_function or len(sLog) == 0:
            return
        return self.loging_function(sLog + '\n')

    def stop_realtime_application(self):
        # Platform.RealTimeApplication ist beim SCALEXIO-Platform-Objekt (Type 22) eine
        # einzelne IPmControllableRealTimeApplication-Property, keine indizierbare Collection
        # (siehe ControlDeskAutomation.pdf, SCALEXIOPlatform / IPmSCALEXIOPlatform <<Interface>>).
        self.main_platform.RealTimeApplication.Stop()

    def start_realtime_application(self):
        self.main_platform.RealTimeApplication.Start()

    def start_online_calibration(self):
        print("Starting Online Calibration...")
        self.application.CalibrationManagement.StartOnlineCalibration()
        self.online_calibration_state = self.application.CalibrationManagement.State
        return self.online_calibration_state

    def stop_online_calibration(self):
        print("Stopping Online Calibration...")
        self.application.CalibrationManagement.StopOnlineCalibration()
        self.online_calibration_state = self.application.CalibrationManagement.State
        return self.online_calibration_state

    def import_datasets_ins_cd_project(self):
        tk.messagebox.showinfo(
            "Select Dataset Folder To Import",
            "Please choose the folder that contains your datasets files."
            )
        dataset_folder_path = filedialog.askdirectory(title="Dataset Import")
        if dataset_folder_path:
            hil_cabs = {}
            for platform in self.main_platform.Platforms:
                hil_cabs[platform.VariableDescriptions[0].Name] = platform
            for dataset_filename in os.listdir(dataset_folder_path):
                dataset_path = os.path.join(dataset_folder_path, dataset_filename)
                if os.path.isfile(dataset_path) and dataset_path.lower().endswith(".cdfx"):
                    for event, element in etree.iterparse(dataset_path, html=True, events=("start", "end")):
                        if event == "end":
                            if element.tag == "sw-system":
                                for child in element.iter():
                                    if child.tag == "short-name":
                                        dataset_cab = child.text
                                        if dataset_cab in hil_cabs:
                                            element.clear()
                                            datasets_from_cab = [dataset.FileName for dataset in hil_cabs[dataset_cab].ActiveVariableDescription.DataSets]
                                            if dataset_filename in datasets_from_cab:
                                                dataset_filename = unique_file_name(dataset_filename, datasets_from_cab)
                                                print(f"New Dataset Name: {dataset_filename}")
                                            hil_cabs[dataset_cab].ActiveVariableDescription.DataSets.Import(dataset_path)
                                            dataset = hil_cabs[dataset_cab].ActiveVariableDescription.DataSets.Item(dataset_filename)
                                            dataset.AutomaticDownloadEnabled = True
                                            if self.online_calibration_state == 1:
                                                dataset.WriteToHardware()
                                            print(f"{dataset_filename} is imported into {dataset_cab}")

def parse_decimal_string_to_int(sInput:str):
    try:
        return int(float(sInput))
    except ValueError:
        print(f"Cannot convert '{sInput}' to a number.")
        return None

def unique_file_name(file_name:str, file_list:list):
    """
    Returns a unique file name by adding _1, _2, ... if needed.
    """
    base, ext = os.path.splitext(file_name)
    counter = 1
    new_file_name = f"{base}_{counter}{ext}"
    while new_file_name in file_list:
        counter += 1
        new_file_name = f"{base}_{counter}{ext}"
    return new_file_name