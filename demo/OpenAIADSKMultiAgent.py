from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
import os
import mailer_config as cfg
import asyncio
import smtplib # Added for SMTP
from email.mime.text import MIMEText # Added for creating email messages
from email.mime.multipart import MIMEMultipart # Added for supporting HTML and plain text

# Import configuration from mailer_config.py
import mailer_config

###############################################################
## PARAMETERS
###############################################################
v_model = "gpt-4o-mini"
load_dotenv(override=True)

# 1. workflow with agents
# 2. workflow with agent and tool
# 3. agent calling other agents (tools or handsoff)

# 1. workflow with agents
# defining the instructions

instructie1 = "Je naam is Ilse Degroot, ilse@syvilledesigns.com, +32 495 590816. Je bent een vriendelijke maar super-degelijke sales agent bij Syville Designs, \
een bedrijf dat gepersonaliseerde premium geschenken maakt zoals snijplanken en wijnkisten. \
Je hebt heel veel ervaring in het verkopen van luxe merken en premium geschenken te verkopen aan grote bedrijven. \
Je schrijft uiterst professionele, formele cold e-mails, perfect voor grote bedrijven die niets aan het toeval overlaten. \
Je sluit altijd af met een positieve groet en een glimlach. Je spreekt in het Nederlands."

instructie2 = "Je naam is Erik van der Veen, erik@syvilledesigns.com, +32 495 590816. Je bent een creatieve en speelse sales agent bij Syville Designs, \
waar je met humor en lef iedereen warm maakt voor unieke, gepersonaliseerde geschenken. \
Je schrijft originele en vrolijke cold e-mails die de lezer laten glimlachen én meteen zin geven om een gepersonaliseerde snijplank te bestellen. Durf te verrassen en wees nét een tikkeltje gek. Je spreekt in het Nederlands."

instructie3 = "Je naam is Patrick Bal, patrick@syvilledesigns.com, +32 495 590816. Je bent een ultrakorte, to-the-point sales agent bij Syville Designs, \
waar je gelooft in 'minder woorden, meer impact'. \
Je schrijft supersnelle, directe cold e-mails zonder omwegen, ideaal voor drukbezette ondernemers. Je bent recht door zee, maar sluit toch af met een kleine knipoog ;). Je spreekt in het Nederlands."

###############################################################
## AGENTS
###############################################################
sales_agent_premium = Agent(
    name="Sales Agent Premium",
    instructions=instructie1,
    tools=[],
    model=v_model
)

sales_agent_fun = Agent(
    name="Sales Agent Fun",
    instructions=instructie2,
    tools=[],
    model=v_model
)

sales_agent_short = Agent(
    name="Sales Agent Short",
    instructions=instructie3,
    tools=[],
    model=v_model
)
    
async def run_one_agents():
    # this starts the agent
    v_user_prompt= "Schrijf een cold email naar de CEO van het software bedrijf Sirus, Gert De Tant"
    result = Runner.run_streamed(starting_agent=sales_agent_premium, input=v_user_prompt)
    # this is the stream of events: Instead of waiting for the whole answer, you get parts (chunks) of the email as soon as they are generated.
    # It loops through each chunk as it arrives:
    async for event in result.stream_events():  
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

            # raw_response_event	The agent generated some output text
            # tool_call_event	    The agent is calling a tool
            # tool_result_event	    The result from the tool call
            # error_event	        An error happened
            # function_call_event	The agent is calling a custom function
            # function_result_event	Result from the custom function
            # agent_action_event	Agent switches task, hands off, or acts in some way
            # final_response_event	The agent is done, streaming is finished
            
            # ResponseTextDeltaEvent is an event type (a class or object) used in streaming AI agent responses.
            # It represents a piece (delta/chunk) of the text the agent is generating as its response.
            # In streaming, the full answer is sent in small parts (deltas) as the model generates them, rather than all at once at the end.

async def run_all_sales_agents():
    
    v_user_prompt= "Schrijf een cold email naar de CEO van het software bedrijf Sirus, Gert De Tant"
    with trace("All Sales Agents"):
        results  = await asyncio.gather(
            Runner.run(sales_agent_premium, v_user_prompt),
            Runner.run(sales_agent_fun, v_user_prompt),
            Runner.run(sales_agent_short, v_user_prompt)
        )
        outputs = [result.final_output for result in results]
        # Print the results
        for output in outputs:
            print(output)


async def send_email_smtp(to_email: str, from_email: str, subject: str, body: str, content_type: str = "text/plain"):
    """
    Sends an email using SMTP.

    Args:
        to_email (str): The recipient's email address.
        from_email (str): The sender's email address. This should match EMAIL_USER in .env if authentication is required.
        subject (str): The subject of the email.
        body (str): The body of the email.
        content_type (str): The content type of the email, "text/plain" or "text/html".
                            Defaults to "text/plain".
    """
    email_user = cfg.EmailConfig.FROM_ADDR
    email_password = os.environ.get("EMAIL_PWD")

    if not email_user or not email_password:
        print("Error: EMAIL_USER or EMAIL_PASSWORD not found in environment variables.")
        return False

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with the appropriate content type
    if content_type == "text/html":
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    try:
        def _send_mail():
            server = None
            if cfg.EmailConfig.USE_SSL:
                server = smtplib.SMTP_SSL(cfg.EmailConfig.SMTP_SERVER, cfg.EmailConfig.SMTP_PORT)
            else:
                server = smtplib.SMTP(cfg.EmailConfig.SMTP_SERVER, cfg.EmailConfig.SMTP_PORT)
            
            if cfg.EmailConfig.USE_TLS:
                server.starttls() # Secure the connection
            
            # Login to the server
            # Note: from_email should typically be the same as email_user for authentication
            server.login(email_user, email_password)
            
            # Send the email
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print(f"Email sent successfully to {to_email} via SMTP!")

        await asyncio.to_thread(_send_mail)
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}. Check your email user/password and SMTP settings.")
        print("Ensure 'Less secure app access' is enabled if using Gmail, or use an App Password.")
        return False
    except Exception as e:
        print(f"Error sending email via SMTP: {e}")
        return False

# Example usage (uncomment to test):
async def test_email():
    # Ensure EMAIL_USER and EMAIL_PASSWORD are set in your .env file
    # and mailer_config.py is configured correctly.
    success = await send_email_smtp(
        to_email=cfg.EmailConfig.TO_ADDR,
        from_email=cfg.EmailConfig.FROM_ADDR,
        subject="Test Email via SMTP",
        body="<h1>Hello!</h1><p>This is a test email sent via SMTP using Python.</p><p>This is <b>HTML</b> content.</p>",
        content_type="text/html"
    )
    # Test plain text
    success = await send_email_smtp(
        to_email=cfg.EmailConfig.TO_ADDR,
        from_email=cfg.EmailConfig.FROM_ADDR,
        subject="Test Plain Text Email via SMTP",
        body="Hello!\nThis is a plain text email sent via SMTP using Python.",
        content_type="text/plain"
    )
    if success:
        print("Email task completed successfully.")
    else:
        print("Email task failed.")

async def main():
    #await test_email()
    # await run_agents()
    await run_all_sales_agents()

if __name__ == "__main__":
    asyncio.run(main())

