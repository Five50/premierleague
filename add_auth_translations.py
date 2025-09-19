#!/usr/bin/env python3
"""
Script to add Swedish translations for authentication strings to django.po
"""

import re

# Read the current django.po file
with open('locale/sv/LC_MESSAGES/django.po', 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary of translations for authentication strings
translations = {
    "Welcome Back": "Välkommen Tillbaka",
    "Sign in to access your football dashboard": "Logga in för att komma åt din fotbollstavla",
    "Password": "Lösenord",
    "Enter your password": "Ange ditt lösenord",
    "Remember me": "Kom ihåg mig",
    "Forgot password?": "Glömt lösenordet?",
    "Please correct the following errors:": "Var vänlig och korrigera följande fel:",
    "New to ALLSVENSKAN Insikter?": "Ny på ALLSVENSKAN Insikter?",
    "Create an account": "Skapa ett konto",
    "Need help?": "Behöver du hjälp?",
    "Email Address": "E-postadress",
    "Enter your email": "Ange din e-postadress",
    "Join the Community": "Gå med i Gemenskapen",
    "Create your account to access exclusive football content": "Skapa ditt konto för att få tillgång till exklusivt fotbollsinnehåll",
    "Erik": "Erik",
    "Svensson": "Svensson",
    "Create a strong password": "Skapa ett starkt lösenord",
    "Password must be at least 8 characters": "Lösenordet måste vara minst 8 tecken",
    "Weak password": "Svagt lösenord",
    "Fair password": "Hyfsigt lösenord",
    "Good password": "Bra lösenord",
    "Strong password": "Starkt lösenord",
    "Confirm Password": "Bekräfta Lösenord",
    "Confirm your password": "Bekräfta ditt lösenord",
    "Passwords do not match": "Lösenorden stämmer inte överens",
    "Send me Allsvenskan news and match updates": "Skicka Allsvenskan-nyheter och matchuppdateringar till mig",
    "Creating account...": "Skapar konto...",
    "Already have an account?": "Har du redan ett konto?",
    "Sign in": "Logga in",
    "Your privacy is important to us": "Din integritet är viktig för oss",
    "All information is encrypted and securely stored. We never share your personal information with third parties.": "All information är krypterad och säkert lagrad. Vi delar aldrig din personliga information med tredje part.",
    "Set New Password": "Ange Nytt Lösenord",
    "Create a strong password for your account": "Skapa ett starkt lösenord för ditt konto",
    "Password Reset Successful!": "Lösenordsåterställning Lyckades!",
    "Reset Password": "Återställ Lösenord",
    "Reset Your Password": "Återställ Ditt Lösenord",
    "We'll send you instructions to reset your password": "Vi skickar instruktioner för att återställa ditt lösenord",
    "Check your email": "Kontrollera din e-post",
    "We've sent password reset instructions to": "Vi har skickat instruktioner för lösenordsåterställning till",
    "Didn't receive the email? Check your spam folder or": "Fick du inte e-postmeddelandet? Kontrollera din skräppostmapp eller",
    "Try again with a different email": "Försök igen med en annan e-postadress",
    "Send Reset Instructions": "Skicka Återställningsinstruktioner",
    "Sending...": "Skickar...",
    "Or": "Eller",
    "Back to Sign In": "Tillbaka till Inloggning",
    "Security Tip": "Säkerhetstips",
    "For your security, password reset links expire after 1 hour. Never share your password reset link with anyone.": "För din säkerhet upphör lösenordsåterställningslänkar efter 1 timme. Dela aldrig din lösenordsåterställningslänk med någon.",
    "Still having trouble accessing your account?": "Har du fortfarande problem att komma åt ditt konto?",
    "Contact Support": "Kontakta Support",
    "Back to homepage": "Tillbaka till startsidan",
    "Swedish Football Central": "Svenska Fotbollscentralen",
    "Enter your registered email": "Ange din registrerade e-postadress",
    "Enter the email address associated with your ALLSVENSKAN Insikter account and we'll send you a link to reset your password.": "Ange e-postadressen som är kopplad till ditt ALLSVENSKAN Insikter-konto så skickar vi dig en länk för att återställa ditt lösenord.",
    "First Name": "Förnamn",
    "Last Name": "Efternamn"
}

# Function to add translation after msgid
def add_translation(content, msgid, msgstr):
    # Pattern to find msgid followed by empty msgstr
    pattern = rf'msgid "{re.escape(msgid)}"\nmsgstr ""'
    replacement = f'msgid "{msgid}"\nmsgstr "{msgstr}"'
    return re.sub(pattern, replacement, content)

# Apply all translations
for english, swedish in translations.items():
    content = add_translation(content, english, swedish)

# Write the updated content back to the file
with open('locale/sv/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
    f.write(content)

print("Swedish translations added successfully!")
print("Don't forget to run: python manage.py compilemessages")