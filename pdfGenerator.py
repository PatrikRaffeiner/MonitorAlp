from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.textlabels import Label

import subprocess
from datetime import date

# imports for font registration
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# font registration
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
#print(c.getAvailableFonts())


class PdfGenerator():


   def setup_doc(self, dump_dir, location):

      today = date.today()
      self.styles = getSampleStyleSheet()
      
      doc = SimpleDocTemplate(dump_dir)
      doc.dump_dir = dump_dir
      doc.location = location
      doc.pageinfo = "%s / %s / %s" % ("MCI", location, today)
      doc.PAGE_WIDTH, doc.PAGE_HEIGHT = A4

      self.subHeadingStyle = ParagraphStyle('subtitle',
                                           fontName="Vera",
                                           fontSize=12,
                                           alignment=0,
                                           #spaceAfter=14,
                                           leading = 15, 
                                           leftIndent = -40)
      
      self.story = [Spacer(1, cm)]
   
      return doc

      

   
   def make_drone_measurement_table(self, drone_measurement, doc):
      def get_displacement(point):
            try: 
               # try to get displacement of target points (also initial measurement)
               dx    = "{:.2f}".format(1000*point.displacement[0])
               dy    = "{:.2f}".format(1000*point.displacement[1])
               dz    = "{:.2f}".format(1000*point.displacement[2])
               dabs  = "{:.2f}".format(1000*point.displacement[3])
               return dx, dy, dz, dabs 
            
            
            except Exception as ex:
               # catch exception if initial measurment points do not have displacement values
               return "-", "-", "-", "-"
   
      # column names 
      table = [["Marker Name", "Distanz Ursprung \n (mm)", "Verschiebung (mm)", "" , "" , "Absolute Verschiebung \n (mm)"], 
                [""           ,  ""                       , "x"              , "y", "z",  ""                    ]]

      tp_over_limit = []
      
      # loop through every target point and create row entries according to column names
      for count, tp in enumerate(drone_measurement.target_points):
         norm_dist = "{:.2f}".format(1000*tp.distance_from_origin)
         dx, dy, dz, dabs = get_displacement(tp)
         row = [tp.name, norm_dist,
                dx, dy, dz, dabs]
         
          
         try: 
            # set global document status, visible on top of page
            doc.label_status = drone_measurement.status

            # create list to highlight possible displacement exceedings
            if tp.status == "Warnung":
               tp_over_limit.append([count, colors.yellow])    
            elif tp.status == "Achtung":
               tp_over_limit.append([count, colors.red])     
         except:
            # initial measurement does not have a displacement therefore also no status
            # exception to catch those cases, but not necessarily an error
            pass
            
         table.append(row)

         



      # format table header row and table layout
      self.table = Table(table)
      self.table.setStyle(TableStyle([
         ("FONTSIZE", (0,0), (-1,-1), 9),
         ("ALIGNMENT", (0,0), (-1,-1), "CENTER"),
         ("SPAN", (2,0), (4,0)),
         ("SPAN", (0,0), (0,1)),
         ("SPAN", (1,0), (1,1)),
         ("SPAN", (5,0), (5,1)),
         ("LINEBEFORE", (1,0), (1,-1), .25, colors.black),
         ("LINEBEFORE", (2,0), (2,-1), .25, colors.black),
         ("LINEBEFORE", (3,1), (3,-1), .25, colors.black),
         ("LINEBEFORE", (4,1), (4,-1), .25, colors.black),
         ("LINEBEFORE", (5,0), (5,-1), .25, colors.black),
         ("LINEBELOW", (0,1), (-1,1), 0.25, colors.black) # horizontal line
         ]))
      

      # highlight background of displacement cells based on 
      # exceeded limit list 
      for target in tp_over_limit:
         self.table.setStyle(TableStyle([
            ("BACKGROUND", 
             (5, target[0] + 2), # +2 is offset for header rows
             (5, target[0] +2 ), # +2 is offset for header rows 
             target[1])
         ]))
      
      


   def make_manual_measurement_table(self, manual_measurement, doc):
      def get_displacement(point):
         try: 
            # try to get displacement (initial point does not have displacement)
            return "{:.2f}".format(point.displacement)
         
         except: 
            # initial measurement does not have a displacement - no error
            return "-"

      dist_over_limit = []


      table = [["Marker Name", "Manuell gemessene Distanz zur Basisplatte", "Längenverschiebung"], 
                ["",             "(mm)",                                      "(mm)"]]


      for count, target_point in enumerate(manual_measurement.target_points):
         try: 
            # set global document status, visible on top of page
            doc.label_status = manual_measurement.status

            # create list to highlight possible displacement exceedings
            if target_point.status == "Warnung":
               dist_over_limit.append([count, colors.yellow])
            elif target_point.status == "Achtung":
               dist_over_limit.append([count, colors.red])

         except: 
            # catch case of no displacement for initial displacement 
            pass


         row = [target_point.name, 
                target_point.measured_distance, 
                get_displacement(target_point)]
         
         table.append(row)


      # format table header and layout
      self.table = Table(table)
      self.table.setStyle(TableStyle([
         ("FONTSIZE", (0,0), (-1,-1), 9),
         ("ALIGNMENT", (0,0), (-1,-1), "CENTER"),
         ("SPAN", (0,0), (0,1)),
         ("LINEBEFORE", (1,0), (1,-1), .25, colors.black),
         ("LINEBEFORE", (2,0), (2,-1), .25, colors.black),
         ("LINEBELOW", (0,1), (-1,1), 0.25, colors.black) # horizontal line
      ]))


      # highlight background of displacement cells based on 
      # exceeded limit list 
      for target in dist_over_limit:
         self.table.setStyle(TableStyle([
            ("BACKGROUND", 
            (2, target[0] + 2), # +2 is offset for header rows
            (2, target[0] +2 ), # +2 is offset for header rows 
            target[1])
         ]))





   def insert_drone_measuremtnt(self, measurement_date, doc):
      # add spacer between previous measurement/title and next measurement
      self.story.append(Spacer(1, cm))
      
      # add measurement (table) to the document
      sub_ttl = Paragraph("Drohnen-Messung vom <br/> " + measurement_date, self.subHeadingStyle)
      
      
      self.story.append(sub_ttl)
      self.story.append(self.table)
      self.story.append(Spacer(1, .5*cm))

      return doc
   

   def insert_manual_measuremtnt(self, measurement_date, doc):
      # add spacer between previous measurement/title and next measurement
      self.story.append(Spacer(1, cm))
      
      # add measurement (table) to the document
      sub_ttl = Paragraph("Manuelle Messung vom <br/> " + measurement_date, self.subHeadingStyle)
      
      
      self.story.append(sub_ttl)
      self.story.append(self.table)
      self.story.append(Spacer(1, .5*cm))

      return doc
      


   def dump(self, doc):
      doc.build(self.story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
      os.startfile(doc.dump_dir)




def myFirstPage(canvas, doc):
   canvas.saveState()
   
   # make title
   canvas.setFont('VeraBd',20)
   canvas.drawCentredString(doc.PAGE_WIDTH/2, doc.PAGE_HEIGHT-3*cm, "Aufzeichnungen")
   canvas.drawCentredString(doc.PAGE_WIDTH/2, doc.PAGE_HEIGHT-4*cm, doc.location)  
   
   # make footer
   canvas.setFont('VeraIt',9)
   canvas.drawString(1.5*cm, 1.5*cm, doc.pageinfo)
   
   # make logo
   canvas.drawImage("Innsbruck_Austria-positive_Print.png", 
               doc.PAGE_WIDTH-3.5*cm, doc.PAGE_HEIGHT-2*cm, 
               width=100.4, height=53.2) # orig size = 1004 x 532
   
   draw_status_label(canvas, doc)

   canvas.restoreState()
   



def myLaterPages(canvas, doc):
   canvas.saveState()

   # make footer
   canvas.setFont('VeraIt',9)
   canvas.drawString(1.5*cm, 1*cm, doc.pageinfo)
   
   # make logo
   canvas.drawImage("Innsbruck_Austria-positive_Print.png", 
               doc.PAGE_WIDTH-3.5*cm, doc.PAGE_HEIGHT-2*cm, 
               width=100.4, height=53.2) # orig size = 1004 x 532
   
   # make indicator 
   draw_status_label(canvas, doc)

   canvas.restoreState()





def draw_status_label(canvas, doc):
   try: 
      status = doc.label_status
      if status == "OK":
         label_color = colors.green
      elif status == "Warnung":
         label_color = colors.yellow
      elif status == "Achtung":
         label_color = colors.red

   except: # no status if initial measurmenet
      status = ""
      label_color = colors.white




   # make measurement status icon 
   rect_width = 50
   rect_height = 80
   x = 50
   y = doc.PAGE_HEIGHT-rect_height
   
   canvas.setFillColor(label_color)
   canvas.rect(x, y, rect_width, rect_height, stroke=0, fill=1)
   canvas.setFillColor("black")
   canvas.drawCentredString(x+rect_width/2, y+5, status)


 

   