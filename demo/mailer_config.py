# Applicatienaam voor logging
APP_NAME = "Mail_Tool"

# Add module-level docstring
"""
Email configuration module for Mail_Tool application.
Contains configuration constants for email server settings and Excel processing.
"""

###############################################################################
## Email Configuratie
###############################################################################
# Group related constants into classes or dataclasses for better organization
class EmailConfig:
    """Email server and account configuration."""
    IMAP_SERVER = 'imap.stackmail.com'
    IMAP_PORT = 993
    SMTP_SERVER = 'smtp.stackmail.com'
    SMTP_PORT = 465
    USE_SSL = True
    USE_TLS = False
    EMAIL_ACCOUNT = 'automation@syssauw.com'
    EMAIL_DRAFT_FOLDER = 'Drafts'  # Or 'Concepts' depending on your email client
    TO_ADDR = 'jan.syssauw@syssauw.com'
    FROM_ADDR = 'automation@syssauw.com'
    CC_ADDR = 'automation@syssauw.com'

    EMAIL_TEMPLATE_HTML = 'email_template.html'     ## in same folder as FOLDER Parameter below
    EMAIL_SUBJECT_TEMPLATE = 'IMPORTANT: Hi #VoorNaam#, who\'s working in #Bedrijf#, this is for you!'
    EMAIL_TYPE = 'html'                            ## 'plain' or 'html'

class EmailDefaults:
    """Default email content templates."""
    SUBJECT = 'Voorbeeld concept e-mail'
    BODY_PLAIN = """Beste,

Dit is een concept e-mail, aangemaakt via Python. Je kan deze nog nakijken voor verzending.

Met vriendelijke groeten,
Jouw Naam
"""
    BODY_HTML = """
    <html>
      <body>
        <h1 style="color:blue;">Hello!</h1>
        <p>This is an <b>HTML</b> email sent from <i>Python</i>.</p>
      </body>
    </html>
    """ 

###############################################################################
## XLS Configuratie
###############################################################################
# Group related constants into classes or dataclasses for better organization
class ExcelConfig:
    """Excel file processing configuration."""
    FOLDER = r'D:\projects\C001-Mibosol-P0001-ContactList\data'      ##with ending \
    FILE_NAME = 'participant_list.xlsx'
    SHEET_NAME = 'Data'
    MAX_ROWS = 500
    
    # Column configurations
    MAIL_STATUS_COLUMN = 'Mail Status'
    MAIL_STATUS_UPDATED_COLUMN = "Updated"
    MAIL_STATUS_NEW = 'Ready To Draft'
    MAIL_STATUS_PROCESSED = 'Drafted'
    
    VOORNAAM_COLUMN = 'VoorNaam'
    ACHTERNAAM_COLUMN = 'AchterNaam'
    BEDRIJF_COLUMN = 'Bedrijf'
    EMAIL_COLUMN = 'Email'
    
    # Optional columns
    VAR1_COLUMN = 'Urgentie'
    VAR2_COLUMN = 'To_Contact'
    VAR3_COLUMN = ''
    VAR4_COLUMN = ''
    VAR5_COLUMN = ''


