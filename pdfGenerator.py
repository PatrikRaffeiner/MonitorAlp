from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.textlabels import Label

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

# local imports
from gui import *

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
      table = [["Marker Name", getText("pdf_txt_distOrig"), getText("pdf_txt_shift"), "" , "" , getText("pdf_txt_absShift")], 
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


      # add limits to measurement table
      limit_bar = self.make_limit_bar(drone_measurement)
      temp = [[self.table, "", limit_bar]]
      self.table = Table(temp)

      
      


   def make_manual_measurement_table(self, manual_measurement, doc):
      def get_displacement(point):
         try: 
            # try to get displacement (initial point does not have displacement)
            return "{:.2f}".format(point.displacement*1000) # in millimeters
         
         except: 
            # initial measurement does not have a displacement - no error
            return "-"

      dist_over_limit = []


      table = [["Marker Name", getText("pdf_txt_manDist"), getText("pdf_txt_lenShift")], 
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
                "{:.2f}".format(target_point.measured_distance*1000), # distance in millimeters 
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

      # add limits to measurement table
      limit_bar = self.make_limit_bar(manual_measurement)
      temp = [[self.table, "", limit_bar]]
      self.table = Table(temp)



   def make_limit_bar(self, measurement):
      bar = [[getText("pdf_txt_limit"),"","",""],
             ["","","",""],
             ["","",str(measurement.limit*1000/2) + " mm", ""],
             ["","","", ""],
             ["","",str(measurement.limit*1000) + " mm", ""],
             ["","","", ""],
             ["","","",""]]
      
      colWidths = (.2*cm, .2*cm, .3*cm, .5*cm)
      rowHeights = (.6*cm, .3*cm, .3*cm, .3*cm, .3*cm, .3*cm, .3*cm)
      
      limit_bar = Table(bar, colWidths=colWidths, rowHeights=rowHeights)
      limit_bar.setStyle(TableStyle([
         ("FONTSIZE", (0,0), (-1,-1), 6),
         ("SPAN", (2,2), (3,3)),    # first limit (green/yellow)
         ("SPAN", (2,4), (3,5)),    # second limit (yellow/red)
         ("SPAN", (0,0), (-1,0)),   # header
         ("ALIGNMENT", (0,0), (-1,-1), "CENTER"),
         ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
         ("VALIGN", (0,0), (-1,0), "TOP"),      # header
         ("LINEBEFORE", (0,1), (0,-1), .25, colors.black),  # vertical bar line left  
         ("LINEBEFORE", (1,1), (1,-1), .25, colors.black),  # vertical bar line right
         ("LINEABOVE", (0,1), (0,1), .25, colors.black),    # horizontal bar line top 
         ("LINEBELOW", (0,2), (2,2), .25, colors.black),    
         ("LINEBELOW", (0,4), (2,4), .25, colors.black),
         ("LINEBELOW", (0,-1), (0,-1), .25, colors.black),
         ("BACKGROUND", (0,1), (0,2), colors.green), 
         ("BACKGROUND", (0,3), (0,4), colors.yellow),
         ("BACKGROUND", (0,5), (0,6), colors.red),
         #("GRID", (0,0), (-1,-1), .25, colors.gray)
      ]))

      return limit_bar



   def insert_drone_measuremtnt(self, measurement, doc):
      # add spacer between previous measurement/title and next measurement
      self.story.append(Spacer(1, cm))
      
      # add measurement (table) to the document
      sub_ttl = Paragraph(getText("pdf_txt_titleD") + measurement.date, self.subHeadingStyle)
      
      # make page content
      self.story.append(sub_ttl)       # subtitle
      self.story.append(self.table)    # measurement table incl. limits
      self.story.append(Spacer(1, .1*cm))  

      # add temperature & weather conditions (image) 
      self.story.append(Paragraph('<para>' + getText("meas_txt_temp") + "&nbsp;" +str(measurement.temperature) + '<br/>' +\
                                  getText("meas_txt_weather") + "&nbsp;" + getText("meas_txt_" + str(measurement.weather_conditions)) + \
                                  "&nbsp;" + "&nbsp;" + "&nbsp;" + '<img src="./imgs/' + \
                                  measurement.weather_conditions + \
                                  '.png"width="18" height="18"/> </para>'))
      self.story.append(Spacer(1, .1*cm))
      self.story.append(Paragraph(getText("meas_txt_comment") + ":" ))  
      for line in measurement.comment.splitlines():
         self.story.append(Paragraph(line)) 
      self.story.append(Spacer(1, .5*cm))

      return doc
   


   def insert_manual_measuremtnt(self, measurement, doc):
      # add spacer between previous measurement/title and next measurement
      self.story.append(Spacer(1, cm))
      
      # add measurement (table) to the document
      sub_ttl = Paragraph(getText("pdf_txt_titleM") + measurement.date, self.subHeadingStyle)

      # adding error margin and user comments below table
      self.story.append(sub_ttl)
      self.story.append(self.table)
      self.story.append(Spacer(1, .1*cm))  

      # add temperature & weather conditions (image) 
      self.story.append(Paragraph('<para>' + getText("meas_txt_temp") + "&nbsp;" +str(measurement.temperature) + '<br/>' +\
                                  getText("meas_txt_weather") + "&nbsp;" + getText("meas_txt_" + str(measurement.weather_conditions)) + \
                                  "&nbsp;" + "&nbsp;" + "&nbsp;" + '<img src="./imgs/' + \
                                  measurement.weather_conditions + \
                                  '.png"width="18" height="18"/> </para>'))
      self.story.append(Spacer(1, .1*cm))
      self.story.append(Paragraph(getText("meas_txt_comment") + ":" ))
      for line in measurement.comment.splitlines():
         self.story.append(Paragraph(line)) 
      self.story.append(Spacer(1, .5*cm))

      return doc
      



   def dump(self, doc):
      doc.build(self.story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
      os.startfile(doc.dump_dir)




def myFirstPage(canvas, doc):
   canvas.saveState()
   
   # make title
   canvas.setFont('VeraBd',20)
   canvas.drawCentredString(doc.PAGE_WIDTH/2, doc.PAGE_HEIGHT-3*cm, getText("pdf_txt_title"))
   canvas.drawCentredString(doc.PAGE_WIDTH/2, doc.PAGE_HEIGHT-4*cm, doc.location)  
   
   # make footer
   canvas.setFont('VeraIt',9)
   canvas.drawString(1.5*cm, 1.5*cm, doc.pageinfo)
   
   # make logo
   canvas.drawImage("imgs/Innsbruck_Austria-positive_Print.png", 
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
   canvas.drawImage("imgs/Innsbruck_Austria-positive_Print.png", 
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
   rect_width = 40
   rect_height = 60
   x = 50
   y = doc.PAGE_HEIGHT-rect_height
   
   canvas.setFillColor(label_color)
   canvas.rect(x, y, rect_width, rect_height, stroke=0, fill=1)
   canvas.setFillColor("black")
   canvas.drawCentredString(x+rect_width/2, y+5, status)


 

   