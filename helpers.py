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
            "" : ["", ""],
            "browse_btn" : ["Browse", "Durchsuchen"],
            "hm_txt_title" : ["Monitoring Tool for Alpine Infrastructure", "Monitoring Tool für Alpine Infrastruktur"], 
            "hm_btn_start" : ["Start New Project", "Neues Projekt Starten"],
            "hm_btn_load" : ["Load Project", "Projekt Laden"], 
            "setup_tip_exe" : ["Please find the path to your Reality Capture installation/execution (RealityCapture.exe)", "Bitte den Pfad zur Reality Capture Ausführungsdatei (RealityCapture.exe) angeben"],
            "setup_tip_wrongName" : ["The provided project name /location is already existing. Please rename the project or load the desired project.", "Der angegebene Projektname / Standort existiert bereits. Ändern Sie den Projektnamen oder laden Sie das gewünschte Projekt."],
            "setup_txt_name" : ["Project Name / Location Name", "Projektname / Klettersteigname"],
            "setup_cbx_licence" : ["Existing Licence", "Lizenz vorhanden"],
            "pjct_txt_name" : ["Please enter the name of the project or the location where the measurement was conducted", "Bitte geben Sie den Namen des Projekts oder des Klettersteigs ein."],
            "pjct_txt_RC" : ["Please find the installation execution of your RealityCapture software ", "Bitte geben Sie den Pfad zur Ausführungsdatein von RealityCapture an"],
            "pjct_tip_wrongRC" : ["Incorrect path. Please find the path to your RealityCapture installation and select RealityCapture.exe", "Falscher Pfad. Bitte den Pfad zur RealityCapture-Installation angeben und RealityCapture.exe auswählen"],
            "pjct_cbx_licence" : ["Please check the box if your Reality Capture licence is already installed", "Bitte das Auswahlfeld ankreuzen wenn bereits eine Lizenz vorhanden ist"],
            "pjct_txt_warnremove" : ["Caution! This would delete the folders/files including: \n", "Achtung! Das würde die folgenden Ordner/Dateien löschen: \n"],
            "pjct_btn_rmvall" : ["Remove All", "Alle Löschen"], 
            "pjct_btn_rmvhigh" : ["Remove Highlighted", "Markierte Löschen"],
            "pjct_pop_nowritepre" : ["File is not writable. Please close ", "Datei ist nicht beschreibbar. Bitte schließen Sie "],
            "pjct_pop_nowritepost" : [" and continue.", " und fahren Sie fort."],
            "pjct_pop_wait" : ["Copying images to new measurement folder. This can take a moment", "Kopieren der Bilder in neuen Messungsordner. Das kann einen Moment dauern"],
            "setup_win_title" : ["Project Setup", "Projekt Setup"],
            "init_tip_imgs" : ["Please find the location of your image folder", "Bitte den Pfad zum Bild-Ordner angeben"],
            "init_tip_proj" : ["Please find the location of your disired project folder", "Bitte den Pfad des gewünschten Projekt-Ordners angeben"],
            "init_txt_img" : ["Image Folder", "Bild-Ordner"],
            "init_txt_proj" : ["Project Folder", "Projekt-Ordner"],
            "init_pop_img" : ["Folder does not contain any images or supported images", "Der Ordner enthält keine Bilder oder ein Format das nicht unterstützt wird"],
            "init_pop_projcet" : ["Provided project name is already existing in the current project folder", "Der Ordner enthält bereits einen Projekt mit dem angegeben Projektnamen"],
            "init_win_title" : ["Measurement Setup", "Messung Setup"],
            "lic_txt_file" : ["Licence File", "Lizenz Datei"],
            "lic_txt_pin" : ["Insert PIN", "Bitte PIN eingeben"],
            "lic_text_desc" : ["Please find an existing licence or insert PIN to buy a licence for your images", "Bitte die Lizenz-Datei angeben oder PIN eingeben um Lizenz für verwendete Bilder zu erwerben"],
            "lic_txt_pay" : ["Pay", "Bezahlen"],
            "lic_win_title" : ["Browse Licence", "Lizenz Browse"],
            "mrk_tip_dist" : ["Please provide the reference distance in millimeters inthe format: xxx.x", "Bitte eine Referenz-Distanz in Millimeter im Format xxx.x eingeben"],
            "mrk_tip_man_dist" : ["Please provide the manually measured distance in millimeters in the format: xxx.x", "Bitte die gemessene Distanz in Milllimeter im Format xxx.x eingeben"],
            "mrk_tip_wrongdist" : ["Incorrect format, must be xxx.x", "Falsches Format, bitte im Format xxx.x eingeben"],
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
            "meas_btn_add" : ["Add", "Hinzufügen"],
            "meas_btn_calc" : ["Displacement", "Verschiebung"],
            "meas_btn_comment" : ["Comment", "Kommentar"],
            "meas_btn_openRC" : ["Open in RC", "In RC öffnen"],
            "meas_btn_del" : ["Delete", "Löschen"],
            "meas_win_title" : [" Measurement Overview", " Messung Übersicht"],
            "meas_txt_typeD" : [["Type:", "Drone"], ["Typ:", "Drohne"]],
            "meas_txt_typeM" : [["Type:", "Manual"], ["Typ:", "Händisch"]],
            "meas_txt_loc" : ["Location:", "Standort:"],
            "meas_txt_d&t" : ["Date & Time:", "Datum & Uhrzeit"],
            "meas_txt_refM" : ["Reference Marker:", "Referenz-Marker:"],
            "meas_txt_trgtM" : ["Target Marker:", "Ziel-Marker:"],
            "meas_txt_comment" : ["Comment:", "Kommentar:"],
            "meas_del_warn" : ["Are you sure? This will delete the measurement irreversibly!", "Sind Sie sicher? Die Messung wird damit unwiderruflich gelöscht!"],
            "meas_pop_added" : ["Successfully added measurement to project", "Messung erfolgreich zu Projekt hinzugefügt"],
            "manMeas_txt_desc" : ["Please provide the distance between each target and the base-plate in millimeters:", "Bitte geben Sie die Distanz zwischen jedem Ziel-Marker und der Basis-Platte in Millimeter an:"],
            "manMeas_win_title" : ["Manual Measurement Input", "Eingabe Händische Messung"],
            "disp_txt_trgt" : ["Target Name", "Ziel-Marker"],
            "disp_txt_dist" : ["Distance to origin (mm)", "Distanz zur Basis (mm)"],
            "disp_win_title" : ["Displacements", "Verschiebungen"],
            "pjlist_txt_pjcts" : ["Projects", "Projekte"],
            "pjlist_win_title" : ["Load Projects", "Projekte Laden"],
            "pjlist_btn_del" : ["Delete Project", "Projekt Löschen"],
            "pjlist_btn_load" : ["Load Project", "Projekt Laden"],
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



