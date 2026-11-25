"""PDF scenario report generation."""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def build_pdf_report(name,category,params,result):
    buff=BytesIO()
    doc=SimpleDocTemplate(buff,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm)
    s=getSampleStyleSheet()
    s.add(ParagraphStyle(name="Brand",parent=s["Title"],textColor=colors.HexColor("#176b87"),fontSize=22,leading=27))
    story=[Paragraph("UrbanTwin AI",s["Brand"]),Paragraph("Simulate Today. Shape Tomorrow.",s["Italic"]),
           Spacer(1,8*mm),Paragraph("Scenario Simulation Report",s["Heading1"]),
           Paragraph(f"<b>Scenario:</b> {name}<br/><b>Category:</b> {category}",s["BodyText"]),Spacer(1,5*mm),
           Paragraph("Problem description",s["Heading2"]),Paragraph(result["explanation"],s["BodyText"]),Spacer(1,4*mm),
           Paragraph("Input parameters",s["Heading2"])]
    rows=[["Parameter","Value"]]+[[str(k).replace("_"," ").title(),str(v)] for k,v in params.items()]
    t=Table(rows,colWidths=[75*mm,85*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1e4c72")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),.4,colors.grey),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#eef4f8")]),
        ("FONTSIZE",(0,0),(-1,-1),8),("PADDING",(0,0),(-1,-1),6)]))
    story += [t,Spacer(1,5*mm),Paragraph("Simulation results",s["Heading2"])]
    rows=[["Indicator","Baseline","Projected","Change","Severity"],
          [result["metric"],str(result["baseline"]),str(result["projected"]),str(result["change"]),result["severity"]]]
    t=Table(rows,colWidths=[42*mm,28*mm,28*mm,28*mm,28*mm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1e4c72")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),.4,colors.grey),("FONTSIZE",(0,0),(-1,-1),7.5),("PADDING",(0,0),(-1,-1),6)]))
    story += [t,Spacer(1,5*mm),Paragraph("AI analysis",s["Heading2"]),
              Paragraph(result.get("ai_analysis","Not available").replace("\n","<br/>"),s["BodyText"]),
              Spacer(1,5*mm),Paragraph("Recommendations",s["Heading2"])]
    for i,r in enumerate(result.get("recommendations",[]),1):
        story.append(Paragraph(f"{i}. <b>{r['title']}</b> — {r['reason']}",s["BodyText"]))
    story += [Spacer(1,5*mm),Paragraph("Assumptions and limitations",s["Heading2"]),
              Paragraph("This report uses a simplified academic simulation with user-entered hypothetical values. It is not connected to live municipal systems and does not constitute an engineering forecast or official planning advice. Validate inputs, equations and proposed interventions with local data and qualified domain experts.",s["BodyText"]),
              Spacer(1,5*mm),Paragraph("Conclusion",s["Heading2"]),
              Paragraph("The scenario comparison provides an initial way to explore how selected interventions may influence the chosen indicator. Further analysis should include verified datasets, feasibility, costs, equity and environmental impacts.",s["BodyText"])]
    doc.build(story)
    return buff.getvalue()
