class SMPTProvider:
    def __init__(self, email):
        mailinx = email.find("@")
        self.email = email[mailinx:]

    def server(self):
        if self.email == "@gmail.com":
            server = "smtp.gmail.com"
        elif self.email == "@outlook.com":
            server = "smtp.office365.com"
        elif self.email == "@yahoo.com":
            server = "smtp.mail.yahoo.com"
        elif self.email == "@icloud.com":
            server = "smtp.mail.me.com"
        elif self.email == "@aol.com":
            server = "smtp.aol.com"
        elif self.email == "@protonmail.com":
            server = "smtp.protonmail.com"
        elif self.email == "@zoho.com":
            server = "smtp.zoho.com"
        elif self.email == "@gmx.com":
            server = "mail.gmx.com"
        elif self.email == "@fastmail.com":
            server = "smtp.fastmail.com"
        elif self.email == "@rediffmail.com":
            server = "smtp.rediffmail.com"
        else:
            server = ""
        return server
    
    def portSSL(self):
        return 465
    
    def portTSL(self):
        return 587