import csv
from abc import ABC, abstractmethod

from points import *


def set_axes_equal(ax):
    #Make axes of 3D plot have equal scale so that spheres appear as spheres,
    #cubes as cubes, etc.

    #Input
    #  ax: a matplotlib axis, e.g., as output from plt.gca().
    
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])



# function to read csv file and return list of control points
def read_points_from_csv(controlPoint_path):
    points = []
    # read out exported point-coordinates
    with open(controlPoint_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            #print(line)
            name = line[0]
            x = line[1]
            y = line[2]
            z = line[3]
            #print(f"name: {name}, x: {x}, y: {y}, z: {z}")
            points.append(DronePoint(name, x, y, z))
    
    return points



class TextReadOut(ABC):
    # abstract class to serve as super class for language handling 
    def __init__(self):
        self.dictionary = { # ID : [EN  ,  DE]
            "continue_btn" : ["Continue", "Weiter"],
            "cancel_btn" : ["Cancel", "Abbruch"],
            "acknowl_btn" : ["Acknowledge", "Bestätigen"],
            "warn_btn" : ["Warning!", "Achtung!"],
            "pop_txt_nopjct" : ["No recent projects existent", "Noch keine Projekte gespeichert"],
            "browse_btn" : ["Browse", "Durchsuchen"],
            "hm_txt_title" : ["Monitoring Tool for Alpine Infrastructure", "Monitoring Tool für Alpine Infrastruktur"], 
            "hm_btn_start" : ["Start New Project", "Neues Projekt Starten"],
            "hm_btn_load" : ["Load Project", "Projekt Laden"], 
            "hm_txt_warnRC" : ["An error occurred during the execution of Reality Capture.\nPossibly due to a corrupted marker detection.\nFor more information please inspect the error message from Reality Capture.", 
                               "Während der Ausführung von Reality Capture ist ein Fehler aufgetreten.\nVermutlich durch eine fehlerhafte Marker-Detektion.\nFür nähere Informationen überprüfen Sie bitte die Fehlermeldung in Reality Capture."],
            "setup_txt_loc" : ["Location", "Standort"],
            "setup_tip_exe" : ["Please find the path to your Reality Capture installation/execution (RealityCapture.exe)", "Bitte den Pfad zur Reality Capture Ausführungsdatei (RealityCapture.exe) angeben"],
            "setup_tip_wrongName" : ["The provided project name /location is already existing. Please rename the project or load the desired project.", "Der angegebene Projektname / Standort existiert bereits. Ändern Sie den Projektnamen oder laden Sie das gewünschte Projekt."],
            "setup_txt_name" : ["Measurement Location & Block Identifier:", "Messstelle & Block Bezeichnung:"],
            "setup_max_shift" : ["Permissible shift in mm:", "Zulässige Verschiebung in mm:"],
            "setup_max_desc" : ["Please enter the maximal permissible limit of displacement", "Bitte geben Sie die maximal zulässige Verschiebung an"],
            "setup_win_title" : ["Project Setup", "Projekt Setup"],
            "setup_txt_pjct" : ["Please find the folder where your project or project block should be located.\nHere, measurements of a single rock will be saved.\nIf there is more than one rock at the same location, the projects need to be generated seperately", 
                                "Bitte geben Sie den Ordner an in dem ihr Projekt oder Block ihres Projektes gespeichert werden soll.\nHier werden lediglich die Messungen zu einem einzelnen Gesteinsblock gespeichert.\nFalls es mehrere Blöcke im selben Gebiet gibt, müssen diese einzeln erstellt werden."],
            "setup_txt_img" : ["Please find the folder where the images of the initial measurement are placed", "Bitte geben sie den Ordner an an dem sich die Bilder der initialen Messung befinden"],
            "pjct_txt_name" : ["Please enter the name of the project or the location where the measurement was conducted", "Bitte geben Sie den Namen des Projekts oder des Klettersteigs ein"],
            "pjct_txt_RC" : ["Please find the installation execution of your Reality Capture software ", "Bitte geben Sie den Pfad zur Ausführungsdatein von Reality Capture an"],
            "pjct_tip_wrongRC" : ["Incorrect path. Please find the path to your Reality Capture installation and select RealityCapture.exe", "Falscher Pfad. Bitte den Pfad zur Reality Capture-Installation angeben und RealityCapture.exe auswählen"],
            "pjct_cbx_licence" : ["Please check the box if your Reality Capture licence is already installed", "Bitte das Auswahlfeld ankreuzen wenn bereits eine Lizenz vorhanden ist"],
            "pjct_txt_warnremove" : ["Caution! This would delete the folders/files including: \n", "Achtung! Das würde die folgenden Ordner/Dateien löschen: \n"],
            "pjct_btn_rmvall" : ["Remove All", "Alle Löschen"], 
            "pjct_btn_rmvhigh" : ["Remove Highlighted", "Markierte Löschen"],
            "pjct_pop_nowritepre" : ["File is not writable. Please close ", "Datei ist nicht beschreibbar. Bitte schließen Sie "],
            "pjct_pop_nowritepost" : [" and continue.", " und fahren Sie fort."],
            "pjct_pop_wait" : ["Copying images to new measurement folder. This can take a moment", "Kopieren der Bilder in neuen Messungsordner. Das kann einen Moment dauern"],
            "pjct_txt_missMarkr" : ["One or more of the specified markers could not be detected!", "Ein oder mehrere der angegebenen Marker konnten nicht detektiert werden!"],
            "pjct_txt_missRef" : ["Missing reference markers:", "Fehlende Referenz-Marker:"],
            "pjct_txt_missTar" : ["Missing target markers:", "Fehlende Ziel-Marker:"],
            "pjct_txt_instruct" : ["Please ensure the names of the markers above are accurate. Otherwise ensure the above markers are plainly visible in multiple input images.",
                                   "Bitte stellen Sie sicher, dass die Namen der oben angeführten Marker korrekt sind. Anderenfalls überprüfen Sie, dass die Marker in mehreren Bildern deutlich sichtbar sind."],
            "pjct_pop_save" : ["Project Saved!", "Projekt gespeichert!"],
            "props_txt_GPS" : ["GPS Coordinates", "GPS Kooridnaten"],
            "props_txt_GPSinst" : ["Please enter the new GPS values of the project location", "Bitte geben Sie die neuen GPS Daten des Projekt-Standorts ein"],            
            "props_txt_latitude" : ["New latitude:", "Neuer Breitengrad:"],
            "props_txt_longitude" : ["New longtude:", "Neuer Längengrad:"],
            "props_txt_altitude" : ["New altitude:", "Neue Höhenlage:"],
            "props_txt_limit" : ["Shift Limit", "Limit Verschiebung"],
            "props_txt_limitInst" : ["Please enter the new limit of displacement", "Bitte geben Sie das neue Verschiebungs-Limit ein"],            
            "props_txt_weatherInst" : ["Please enter the new temperature and/or select the new weather conditions", "Bitte geben Sie die neue Temperatur ein und/oder wählen Sie die neuen Wetterbedingungen aus"],            
            "props_txt_temperature" : ["New temperature:", "Neue Temperatur:"],
            "props_txt_weather" : ["Select new weather condition:", "Neue Wetterbedingung auswählen:"],
            "init_tip_imgs" : ["Please find the location of your image folder", "Bitte den Pfad zum Bild-Ordner angeben"],
            "init_tip_proj" : ["Please find the location of your disired project folder", "Bitte den Pfad des gewünschten Projekt-Ordners angeben"],
            "init_txt_img" : ["Image Folder", "Bild-Ordner"],
            "init_txt_proj" : ["Project Folder", "Projekt-Ordner"],
            "init_pop_img" : ["Folder does not contain any images or supported images", "Der Ordner enthält keine Bilder oder ein Format das nicht unterstützt wird"],
            "init_pop_projcet" : ["Provided project name is already existing in the current project folder", "Der Ordner enthält bereits einen Projekt mit dem angegeben Projektnamen"],
            "init_win_title" : ["Measurement Setup", "Messung Setup"],
            "mrk_tip_dist" : ["Please provide the reference distance in millimeters inthe format: xxx.x", "Bitte eine Referenz-Distanz in Millimeter im Format xxx.x eingeben"],
            "mrk_tip_man_dist" : ["Please provide the manually measured distance in millimeters in the format: xxx.x", "Bitte die gemessene Distanz in Milllimeter im Format xxx.x eingeben"],
            "mrk_tip_wrongdist" : ["Incorrect format, must be xxx.x", "Falsches Format, bitte im Format xxx.x eingeben"],
            "mrk_tip_name" : ["Please provide the marker name in the format 1x12:0XX", "Bitte den Markernamen im Format 1x12:0XX angeben"],
            "mrk_txt_orig" : ["Origin-marker name", "Name des Basis-Markers"],
            "mrk_txt_hrz" : ["Horizontal-marker name", "Name des horizontalen Markers"],
            "mrk_txt_vtk" : ["Vertical-marker name", "Name des vertikalen Markers"],
            "mrk_txt_dist" : ["Marker Distance in Millimeter", "Referenz-Distanz in Millimeter"],
            "mrk_txt_descO" : ["Please enter the name of the origin reference marker", "Bitte den Namen des Basis-Referenz-Markers eingeben"],
            "mrk_txt_descV" : ["Please enter the name of the horizontal reference marker", "Bitte den Namen des  horizontalen Referenz-Markers eingeben"],
            "mrk_txt_descH" : ["Please enter the name of the vertical reference marker", "Bitte den Namen des  vertikalen Referenz-Markers eingeben"],
            "mrk_txt_descD" : ["Please enter the distance between the reference points in mm", "Bitte die Distanz zwischen zwei Referenz-Marken eingeben (in mm)"],
            "mrk_btn_add" : ["Add Target Marker", "Ziel-Marker hinzufügen"],
            "mrk_txt" : ["Target marker ", "Ziel-Marker "],
            "mrk_txt_pre" : ["Please enter the name of the ", "Bitte den Namen des "],
            "mrk_txt_post" : [". target marker", ". Ziel-Markers eingeben"],
            "mrk_win_title" : ["Reference And Target Marker", "Referenz- und Ziel-Marker"],
            "meas_tip_del" : ["Please select the measurement to delete", "Bitte die zu löschende Messung auswählen"],
            "meas_tip_nodel" : ["Cannot delete initial measurement", "Initiale Messung kann nicht gelöscht werden"],
            "meas_tip_delInfo" : ["Removes selected measurement irreversibly", "Löscht die Messung unwiderruflich"],
            "meas_txt_drone" : ["Drone Measurements", "Drohnen-Messungen"],
            "meas_txt_manual" : ["Manual Measurements", "Manuelle Messungen"],
            "meas_txt_measInfo" : ["Measurement Info", "Messungs Info"],
            "meas_txt_comment" : ["Comment", "Kommentar"],
            "meas_txt_editCmnt" : ["Edit comment", "Kommentar bearbeiten"],
            "meas_txt_acqu" : ["Please enter the date and time when the measurement was taken", "Bitte geben Sie das Datum und die Zeit ein zu der die Messung durchgeführt wurde"],
            "meas_txt_date" : ["Acquisition Date in the format: dd.mm.yyyy", "Erfassungs-Datum im Format: tt.mm.jjjj"],
            "meas_txt_time" : ["Acquisition Time in the formar: hh:mm", "Erfassungs-Zeit im Format: hh:mm"],
            "meas_win_acqu" : ["Acquisition Date & Time", "Erfassungs-Datum & Zeit"],
            "meas_txt_acquT" : ["Acquisition Time:", "Erfassungs-Zeit:"],
            "meas_txt_acquD" : ["Acquisition Date:", "Erfassungs-Datum:"],
            "meas_txt_evalD" : ["Evaluation Date:", "Auswertungs-Datum:"],
            "meas_txt_evalT" : ["Evaluation Time:", "Auswertungs-Zeit:"],
            "meas_txt_numimgs" : ["Number of Images:", "Anzahl Bilder:"],
            "meas_txt_error" : ["Mean Deviation:", "Mittlere Abweichung:"],
            "meas_txt_acc" : ["Accuracy Score:", "Genauigkeits Bewertung:"],
            "meas_menu_prjct" : ["Project", "Projekt"],
            "meas_menu_drone" : ["Drone", "Drohne"],
            "meas_menu_manual" : ["Manual", "Manuell"],
            "meas_menu_addD" : ["Add Measurement::addDrone", "Messung Hinzufügen::addDrone"],
            "meas_menu_addM" : ["Add Measurement::addManual", "Messung Hinzufügen::addManual"],
            "meas_menu_disp" : ["!Show Measurement Displacement::displacement", "!Verschiebung Anzeigen::displacement"],
            "meas_menu_open" : ["!Open Measurement in Reality Capture::openRC", "!Messung in Reality Capture Öffnen::openRC"],
            "meas_menu_cmmntM" : ["!Add/Edit Comment::commentManual", "!Kommentar Hinzufügen/Bearbeiten::commentManual"],
            "meas_menu_cmmntD" : ["!Add/Edit Comment::commentDrone", "!Kommentar Hinzufügen/Bearbeiten::commentDrone"],
            "meas_menu_delM" : ["!Delete Measurement::deleteManual", "!Messung Löschen::deleteManual"],
            "meas_menu_delD" : ["!Delete Measurement::deleteDrone", "!Messung Löschen::deleteDrone"],
            "meas_menu_delP" : ["Delete Project::deleteProject", "Projekt Löschen::deleteProject"],
            "meas_menu_pdfP" : ["Show Project Report::showProjectReport", "Projekt-Bericht Anzeigen::showProjectReport"],
            "meas_menu_pdfM" : ["!Show Measurement Report::showMeasurementReport", "!Messungs-Bericht Anzeigen::showMeasurementReport"],
            "meas_menu_save" : ["Save::save", "Speichern::save"],
            "meas_menu_openPjct" : ["Open Project Folder::openProject", "Projekt-Ordner Öffnen::openProject"],
            "meas_menu_openMeas" : ["!Open Measurement Folder::openMeasurement", "!Messung in Ordner Öffnen::openMeasurement"],
            "meas_menu_map" : ["Show in Map::map", "In Karte Anzeigen::map"],
            "meas_menu_propsM" : ["!Show Measurement Properties::editManualMeasProps", "!Messungseinstellungen anzeigen::editManualMeasProps"],
            "meas_menu_propsD" : ["!Show Measurement Properties::editDroneMeasProps", "!Messungseinstellungen anzeigen::editDroneMeasProps"],
            "meas_menu_props" : ["Show Project Properties::editPrjProps", "Projekteinstellungen anzeigen::editPrjProps"],
            "meas_win_title" : [" Measurement Overview", " Messung Übersicht"],
            "meas_txt_typeD" : [["Type:", "Drone"], ["Typ:", "Drohne"]],
            "meas_txt_typeM" : [["Type:", "Manual"], ["Typ:", "Händisch"]],
            "meas_txt_loc" : ["Location:", "Standort:"],
            "meas_txt_aquD&T" : ["Aquisition Date & Time:", "Erfassungs-Datum & Zeit:"],
            "meas_txt_evalD&T" : ["Evaluation Date & Time:", "Auswertungs-Datum & Zeit:"],
            "meas_txt_weather" : ["Weather Conditions:", "Wetterbedingungen:"],
            "meas_txt_sunny" : ["Sunny", "Sonnig"],
            "meas_txt_partly_cloudy" : ["Partly cloudy", "Teilweise bewölkt"],
            "meas_txt_cloudy" : ["Cloudy", "Bewölkt"],
            "meas_txt_foggy" : ["Foggy", "Nebel"],
            "meas_txt_rainy" : ["Rainy", "Regen"],
            "meas_txt_snowy" : ["Snwowy", "Schneefall"],
            "meas_txt_temp" : ["Temperature:", "Temperatur:"],
            "meas_txt_refM" : ["Reference Marker:", "Referenz-Marker:"],
            "meas_txt_trgtM" : ["Target Marker:", "Ziel-Marker:"],
            "meas_txt_val" : ["Measurement Values", "Messwerte"],
            "meas_txt_dist" : ["New Measurement Distances (mm)", "Neue Distanz (mm)"],
            "meas_new_val" : ["Please enter the new measurement values", "Bitte geben Sie die neuen Messwerte ein"],
            "meas_del_warn" : ["Are you sure? This will delete the measurement irreversibly!", "Sind Sie sicher? Die Messung wird damit unwiderruflich gelöscht!"],
            "manMeas_txt_desc" : ["Please provide the distance between each target and the base-plate in millimeters:", "Bitte geben Sie die Distanz zwischen jedem Ziel-Marker und der Basis-Platte in Millimeter an:"],
            "manMeas_win_title" : ["Manual Measurement Input", "Eingabe Händische Messung"],
            "pprops_win_title" : ["Project Properties", "Projekt Einstellungen"],
            "mprops_win_title" : ["Measurement Properties", "Messungs Einstellungen"],
            "weather_txt_instrW" : ["Please select one of the weather conditions present during the measurement:", "Bitte wählen Sie eine der Wetterbedingungen während der Messung:"],
            "weather_txt_instrT" : ["Please enter the temperature during measurement", "Bitte geben Sie die Temperatur während der Messung an"],
            "weather_win_title" : ["Weather Conditions", "Wetterbedingungen"],
            "disp_txt_trgt" : ["Target Name", "Ziel-Marker"],
            "disp_txt_dist" : ["Distance to origin (mm)", "Distanz zur Basis (mm)"],
            "disp_win_title" : ["Displacements", "Verschiebungen"],
            "pjlist_txt_pjcts" : ["Projects", "Projekte"],
            "pjlist_win_title" : ["Load Projects", "Projekte Laden"],
            "pjlist_btn_del" : ["Delete Project", "Projekt Löschen"],
            "pjlist_btn_load" : ["Load Project", "Projekt Laden"],
            "pdf_pop_proj_create" : ["Successfully created new project", "Neues Projekt erfolgreich erstellt"],
            "pdf_pop_meas_added" : ["Successfully added measurement to project", "Messung erfolgreich zu Projekt hinzugefügt"],
            "pdf_pop_cmnt_added" : ["Successfully added comment to measurement", "Kommentar erfolgreich zu Messung hinzugefügt"],
            "pdf_pop_meas_del" : ["Successfully removed measurement", "Messung erfolgreich gelöscht"],
            "pdf_pop_meas_edit" : ["Successfully edited measurement", "Messung erfolgreich bearbeitet"],
            "pdf_txt_limit" : ["Limits", "Grenzwerte"],
            "pdf_txt_manDist" : ["Manually measured distance to base plate","Manuell gemessene Distanz zur Basisplatte"],
            "pdf_txt_lenShift" : ["Displacement", "Längenänderung"],
            "pdf_txt_meanErr" : ["Mean Error \n (mm)", "Mittlerer \n Fehler \n (mm)"],
            "pdf_txt_distOrig" : ["Distance to origin \n (mm)", "Distanz Ursprung \n (mm)"],
            "pdf_txt_shift" : ["Displacement (mm)", "Verschiebung (mm)"],
            "pdf_txt_absShift" : ["Absolute \n displacement \n (mm)", "Absolute \n Verschiebung \n (mm)"],
            "pdf_txt_titleD" : ["Drone measurement <br/> ","Drohnen-Messung <br/> "],
            "pdf_txt_titleM" : ["Manual measurement <br/> ","Manuelle Messung <br/> "],
            "pdf_txt_title" : ["Records","Aufzeichnungen"],
            "import_txt_title" : ["Import Project","Projekt Importieren"],
            "import_txt_instr" : ["Please browse and select the project file (.pkl) you wish to import","Bitte suchen und wählen Sie die Projekt-Datei (.pkl) aus die importiert werden soll"],
            "import" : ["Import","Importieren"],
            "import_warn_meas" : ["The selected file is a measurement file. Please select a project file","Die ausgewählte Datei ist eine Messung. Bitte wählen Sie eine Projekt-Datei aus"],
            "import_warn_wrongPjct" : ["The selected file is not a project file. Please select a project file","Die ausgewählte Datei ist keine Projekt-Datei. Bitte wählen Sie eine Projekt-Datei aus"],
            }


    @abstractmethod
    def gettext(self, textID):
        pass


class enTextReadOut(TextReadOut):
    # child class for english language readout
    def gettext(self, textID):
        return self.dictionary[textID][0]


class deTextReadOut(TextReadOut):
    # child class for german language readout
    def gettext(self, textID):
        return self.dictionary[textID][1]


# global variable/class
readout = deTextReadOut()



