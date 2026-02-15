"""
Comprehensive test cases for ClairOS database
Covers all 11 domains and 27 subdomains per project requirements [1]
"""

# Test cases organized by domain and subdomain
# Format matches your updated chunk structure with integer chunk_id

TEST_CHUNKS = [
  {
    "chunk_id": "001",
    "domain": "Operational",
    "subdomain": "Project Metadata",
    "text": "Here is our forecast",
    "source": {
      "email_id": "1",
      "to": "tim.belden@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Mon, 14 May 2001 16:39:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Strategic Confidential",
    "subdomain": "Business Strategy",
    "text": "Traveling to have a business meeting takes the fun out of the trip. Especially if you have to prepare a presentation. I would suggest holding the business plan meetings here then take a trip without any formal business meetings. I would even try and get some honest opinions on whether a trip is even desired or necessary.",
    "source": {
      "email_id": "2",
      "to": "john.lavorato@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re:",
      "timestamp": "Fri, 4 May 2001 13:51:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Operational",
    "subdomain": "Project Metadata",
    "text": "As far as the business meetings, I think it would be more productive to try and stimulate discussions across the different groups about what is working and what is not. Too often the presenter speaks and the others are quiet just waiting for their turn. The meetings might be better if held in a round table discussion format.",
    "source": {
      "email_id": "2",
      "to": "john.lavorato@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re:",
      "timestamp": "Fri, 4 May 2001 13:51:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Personal Life",
    "subdomain": "Crisis/Sensitive Content",
    "text": "My suggestion for where to go is Austin. Play golf and rent a ski boat and jet ski's. Flying somewhere takes too much time.",
    "source": {
      "email_id": "2",
      "to": "john.lavorato@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re:",
      "timestamp": "Fri, 4 May 2001 13:51:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "test successful. way to go!!!",
    "source": {
      "email_id": "3",
      "to": "leah.arsdall@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: test",
      "timestamp": "Wed, 18 Oct 2000 03:00:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "HR",
    "subdomain": "All",
    "text": "Can you send me a schedule of the salary and level of everyone in the scheduling group. Plus your thoughts on any changes that need to be made. (Patti S for example)",
    "source": {
      "email_id": "4",
      "to": "randall.gay@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Mon, 23 Oct 2000 06:13:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "Let's shoot for Tuesday at 11:45.",
    "source": {
      "email_id": "5",
      "to": "greg.piper@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: Hello",
      "timestamp": "Thu, 31 Aug 2000 05:07:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "How about either next Tuesday or Thursday?",
    "source": {
      "email_id": "6",
      "to": "greg.piper@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: Hello",
      "timestamp": "Thu, 31 Aug 2000 04:17:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Operational",
    "subdomain": "Org-Structure Metadata",
    "text": "Please cc the following distribution list with updates: Phillip Allen (pallen@enron.com) Mike Grigsby (mike.grigsby@enron.com) Keith Holst (kholst@enron.com) Monique Sanchez Frank Ermis John Lavorato",
    "source": {
      "email_id": "7",
      "to": "david.l.johnson@enron.com, john.shafer@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 22 Aug 2000 07:44:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "any morning between 10 and 11:30",
    "source": {
      "email_id": "8",
      "to": "joyce.teixeira@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: PRC review - phone calls",
      "timestamp": "Fri, 14 Jul 2000 06:59:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Security",
    "subdomain": "Operational Security",
    "text": "1. login: pallen pw: ke9davis I don't think these are required by the ISP",
    "source": {
      "email_id": "9",
      "to": "mark.scott@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: High Speed Internet Access",
      "timestamp": "Tue, 17 Oct 2000 02:26:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "2. static IP address IP: 64.216.90.105 Sub: 255.255.255.248 gate: 64.216.90.110 DNS: 151.164.1.8 3. Company: 0413 RC: 105891",
    "source": {
      "email_id": "9",
      "to": "mark.scott@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: High Speed Internet Access",
      "timestamp": "Tue, 17 Oct 2000 02:26:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Strategic Confidential",
    "subdomain": "Business Strategy",
    "text": "In a Parallon 75 microturbine power generation deal for a national accounts customer, I am developing a proposal to sell power to customer at fixed or collar/floor price. To do so I need a corresponding term gas price for same. Microturbine is an onsite generation product developed by Honeywell to generate electricity on customer site (degen). using natural gas. In doing so, I need your best fixed price forward gas price deal for 1, 3, 5, 7 and 10 years for annual/seasonal supply to microturbines to generate fixed kWh for customer.",
    "source": {
      "email_id": "10",
      "to": "zimam@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "FW: fixed forward or other Collar floor gas price terms",
      "timestamp": "Mon, 16 Oct 2000 06:44:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "We have the opportunity to sell customer kWh 's using microturbine or sell them turbines themselves. kWh deal must have limited/ no risk forward gas price to make deal work. We are proposing installing 180 - 240 units across a large number of stores (60-100) in San Diego. For 6-8 hours a day Microturbine run time: Gas requirement for 180 microturbines 227 - 302 MMcf per year Gas requirement for 240 microturbines 302 - 403 MMcf per year. Gas will likely be consumed from May through September, during peak electric period. Gas price required: Burnertip price behind (LDC) San Diego Gas & Electric Need detail breakout of commodity and transport cost (firm or interruptible).",
    "source": {
      "email_id": "10",
      "to": "zimam@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "FW: fixed forward or other Collar floor gas price terms",
      "timestamp": "Mon, 16 Oct 2000 06:44:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Operational",
    "subdomain": "Org-Structure Metadata",
    "text": "For delivered gas behind San Diego, Enron Energy Services is the appropriate Enron entity. I have forwarded your request to Zarin Imam at EES. Her phone number is 713-853-7107.",
    "source": {
      "email_id": "11",
      "to": "buck.buckner@honeywell.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: FW: fixed forward or other Collar floor gas price terms",
      "timestamp": "Mon, 16 Oct 2000 06:42:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "Here are the rentrolls: Open them and save in the rentroll folder. Follow these steps so you don't misplace these files. 1. Click on Save As 2. Click on the drop down triangle under Save in: 3. Click on the (C): drive 4. Click on the appropriate folder 5. Click on Save:",
    "source": {
      "email_id": "12",
      "to": "stagecoachmama@hotmail.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Fri, 13 Oct 2000 06:45:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "We don't have a single point of contact from the trading group. We've had three meetings which brought out very different issues from different traders. We really need a single point of contact to help drive the trader requirements and help come to a consensus regarding the requirements. We're getting hit with a lot of different requests, many of which appear to be outside the scope of position consolidation.",
    "source": {
      "email_id": "13",
      "to": "keith.holst@enron.com",
      "cc": "Beth Perlman/HOU/ECT@ECT",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Consolidated positions: Issues & To Do list",
      "timestamp": "Mon, 9 Oct 2000 07:16:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "Things requested thus far (no particular order): Inclusion of Sitara physical deals into the TDS position manager and deal ticker. Customized rows and columns in the position manager (ad hoc rows/columns that add up existing position manager rows/columns). New drill down in the position manager to break out positions by: physical, transport, swaps, options. Addition of a curve tab to the position manager to show the real-time values of all curves on which the desk has a position. Ability to split the current position grid to allow daily positions to be shown directly above monthly positions.",
    "source": {
      "email_id": "13",
      "to": "keith.holst@enron.com",
      "cc": "Beth Perlman/HOU/ECT@ECT",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Consolidated positions: Issues & To Do list",
      "timestamp": "Mon, 9 Oct 2000 07:16:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "Ability to properly show curve shift for float-for-float deals; determine the appropriate positions to show for each: Gas Daily for monthly index, Physical gas for Nymex, Physical gas for Inside Ferc, Physical gas for Mid market. Ability for TDS to pull valuation results based on a TDS flag instead of using official valuations. Position and P&L aggregation across all gas desks.",
    "source": {
      "email_id": "13",
      "to": "keith.holst@enron.com",
      "cc": "Beth Perlman/HOU/ECT@ECT",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Consolidated positions: Issues & To Do list",
      "timestamp": "Mon, 9 Oct 2000 07:16:00 -0700 (PDT)"
    }
  },
    {
    "chunk_id": "002",
    "domain": "HR",
    "subdomain": "All",
    "text": "Here are the names of the west desk members by category. The origination side is very sparse.",
    "source": {
      "email_id": "14",
      "to": "david.delainey@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Thu, 5 Oct 2000 06:26:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "35 million is fine",
    "source": {
      "email_id": "15",
      "to": "paula.harris@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: 2001 Margin Plan",
      "timestamp": "Thu, 5 Oct 2000 05:55:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "004",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "Please plan to attend the below Meeting: Topic: Var, Reporting and Resources Meeting Date: Wednesday, October 11th Time: 2:30 - 3:30 Location: EB30C1",
    "source": {
      "email_id": "16",
      "to": "ina.rangel@enron.com",
      "cc": "Rita Hennessy/NA/Enron@Enron, Laura Harder/Corp/Enron@Enron, Kimberly Brown/HOU/ECT@ECT, Araceli Romero/NA/Enron@Enron, Kimberly Hillis/HOU/ECT@ect",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Var, Reporting and Resources Meeting",
      "timestamp": "Wed, 4 Oct 2000 09:23:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Security",
    "subdomain": "Operational Security",
    "text": "mike grigsby is having problems with accessing the west power site. Can you please make sure he has an active password.",
    "source": {
      "email_id": "17",
      "to": "tim.heizenrader@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Fri, 4 May 2001 11:26:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "The property across the street from the Sagewood units in San Marcos is for sale and approved for 134 units. The land is selling for $2.50 per square foot as it is one of only two remaining approved multifamily parcels in West San Marcos, which now has a moratorium on development.",
    "source": {
      "email_id": "18",
      "to": "pallen70@hotmail.com",
      "cc": "Larry Lewter",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Westgate",
      "timestamp": "Tue, 3 Oct 2000 09:30:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "004",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "Several new studies we have looked at show that the rents for our duplexes and for these new units are going to be significantly higher, roughly $1.25 per square foot if leased for the entire unit on a 12-month lease and $1.30-$1.40 psf if leased on a 12-month term, but by individual room.",
    "source": {
      "email_id": "18",
      "to": "pallen70@hotmail.com",
      "cc": "Larry Lewter",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Westgate",
      "timestamp": "Tue, 3 Oct 2000 09:30:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "005",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "If this project is of serious interest to you, please let me know as there is a very, very short window of opportunity. The equity requirement is not yet known, but it would be likely to be $300,000 to secure the land.",
    "source": {
      "email_id": "18",
      "to": "pallen70@hotmail.com",
      "cc": "Larry Lewter",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Westgate",
      "timestamp": "Tue, 3 Oct 2000 09:30:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "005",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "There will be a meeting on Tuesday, Oct. 10th at 4:00pm in EB3270 regarding Storage Strategies in the West. Please mark your calendars.",
    "source": {
      "email_id": "19",
      "to": "ina.rangel@enron.com",
      "cc": "Jean Mrha/NA/Enron@Enron, Monica Jackson/Corp/Enron@ENRON",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Meeting re: Storage Strategies in the West",
      "timestamp": "Tue, 3 Oct 2000 09:15:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "006",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "Please use the second check as the October payment. If you have already tossed it, let me know so I can mail you another.",
    "source": {
      "email_id": "20",
      "to": "bs_stone@yahoo.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 3 Oct 2000 09:13:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Strategic Confidential",
    "subdomain": "Business Strategy",
    "text": "Denver's short rockies position beyond 2002 is created by their Trailblazer transport. They are unhedged 15,000/d in 2003 and 25,000/d in 2004 and 2005. They are scrubbing all their books and booking the Hubert deal on Wednesday and Thursday.",
    "source": {
      "email_id": "21",
      "to": "john.lavorato@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Wed, 20 Sep 2000 08:06:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "004",
    "domain": "Strategic Confidential",
    "subdomain": "Business Strategy",
    "text": "Is there going to be a conference call or some type of weekly meeting about all the regulatory issues facing California this week? Can you make sure the gas desk is included.",
    "source": {
      "email_id": "22",
      "to": "james.steffes@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Wed, 2 May 2001 12:36:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "PII",
    "subdomain": "Contact Identifiers",
    "text": "Full Name: Phillip Allen Login ID: pallen Extension: 3-7041 Office Location: EB3210C",
    "source": {
      "email_id": "23",
      "to": "tori.kuykendall@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: 2- SURVEY - PHILLIP ALLEN",
      "timestamp": "Wed, 2 May 2001 10:27:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "004",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "What type of computer do you have? (Desktop, Laptop, Both) Both Do you have a PDA? If yes, what type do you have: (None, IPAQ, Palm Pilot, Jornada) IPAQ",
    "source": {
      "email_id": "23",
      "to": "tori.kuykendall@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: 2- SURVEY - PHILLIP ALLEN",
      "timestamp": "Wed, 2 May 2001 10:27:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Security",
    "subdomain": "Operational Security",
    "text": "Do you have permission to access anyone's Email/Calendar? NO Does anyone have permission to access your Email/Calendar? YES If yes, who? INA RANGEL",
    "source": {
      "email_id": "23",
      "to": "tori.kuykendall@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: 2- SURVEY - PHILLIP ALLEN",
      "timestamp": "Wed, 2 May 2001 10:27:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "006",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "What are your normal work hours? From: 7:00 AM To: 5:00 PM Will you be out of the office in the near future for vacation, leave, etc? NO",
    "source": {
      "email_id": "23",
      "to": "tori.kuykendall@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: 2- SURVEY - PHILLIP ALLEN",
      "timestamp": "Wed, 2 May 2001 10:27:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "005",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "REASONS FOR USING OUTLOOK WEB ACCESS (OWA) 1. Once your mailbox has been migrated from Notes to Outlook, the Outlook client will be configured on your computer. After migration of your mailbox, you will not be able to send or recieve mail via Notes, and you will not be able to start using Outlook until it is configured by the Outlook Migration team the morning after your mailbox is migrated. During this period, you can use Outlook Web Access (OWA) via your web browser (Internet Explorer 5.0) to read and send mail.",
    "source": {
      "email_id": "24",
      "to": "ina.rangel@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "4-URGENT - OWA Please print this now.",
      "timestamp": "Tue, 1 May 2001 17:14:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "006",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "HOW TO ACCESS OUTLOOK WEB ACCESS (OWA) Launch Internet Explorer 5.0, and in the address window type: http://nahou-msowa01p/exchange/john.doe Substitute john.doe with your first and last name, then click ENTER. You will be prompted with a sign in box. Type in corp/your user id for the user name and your NT password to logon to OWA and click OK.",
    "source": {
      "email_id": "24",
      "to": "ina.rangel@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "4-URGENT - OWA Please print this now.",
      "timestamp": "Tue, 1 May 2001 17:14:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "007",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "Features NOT available using OWA: - Tasks - Journal - Spell Checker - Offline Use - Printing Templates - Reminders - Timed Delivery - Expiration - Outlook Rules - Voting, Message Flags and Message Recall - Sharing Contacts with others - Task Delegation - Direct Resource Booking - Personal Distribution Lists",
    "source": {
      "email_id": "24",
      "to": "ina.rangel@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "4-URGENT - OWA Please print this now.",
      "timestamp": "Tue, 1 May 2001 17:14:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "007",
    "domain": "Scheduling",
    "subdomain": "All",
    "text": "I scheduled a meeting with Jean Mrha tomorrow at 3:30",
    "source": {
      "email_id": "25",
      "to": "ina.rangel@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Wed, 6 Sep 2000 06:04:00 -0700 (PDT)"
    }
  },
    {
    "chunk_id": "006",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "The City of Austin, TX has experienced 300+ MW of load growth this year due to server farms and technology companies. There is a 100 MW server farm trying to hook up to HL&P as we speak and they cannot deliver for 12 months due to distribution infrastructure issues. Obviously, Seattle, Porltand, Boise, Denver, San Fran and San Jose in your markets are in for a rude awakening in the next 2-3 years.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "007",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "In 1997, a little-known Silicon Valley company called Exodus Communications opened a 15,000-square-foot data center in Tukwila. The mission was to handle the Internet traffic and computer servers for the region's growing number of dot-coms. Fast-forward to summer 2000. Exodus is now wrapping up construction on a new 13-acre, 576,000-square-foot data center less than a mile from its original facility.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "008",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "Data centers, also known as co-location facilities and server farms, are sprouting at such a furious pace in Tukwila and the Kent Valley that some have expressed concern over whether Seattle City Light and Puget Sound Energy can handle the power necessary to run these 24-hour, high-security facilities. We are talking to about half a dozen customers that are requesting 445 megawatts of power in a little area near Southcenter Mall. That is the equivalent of six oil refineries.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "009",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "Puget Sound Energy last week asked the Washington Utilities and Transportation Commission to accept a tariff on the new data centers. The tariff is designed to protect the company's existing residential and business customers from footing the bill for the new base stations necessary to support the projects. Those base stations could cost as much as $20 million each.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "010",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "The entire University of Washington, from stadium lights at the football game to the Medical School, averages 31 megawatts per day. We have data center projects in front of us that are asking for 30, 40 and 50 megawatts.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "011",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "With more than 1.5 million square feet, the Intergate complex in Tukwila is one of the biggest data centers. Sabey Corp. re-purchased the 1.35 million square-foot Intergate East facility last September from Boeing Space & Defense. In less than 12 months, the developer has leased 92 percent of the six-building complex to seven different co-location companies. It is probably the largest data center park in the country.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "012",
    "domain": "Research & Development",
    "subdomain": "Technical R&D",
    "text": "Exodus, one of the largest providers of co-location space, plans to nearly double the amount of space it has by the end of the year. We have 2 million square feet of space under construction and we plan to double our size in the next nine months, yet there is more demand right now than data center space.",
    "source": {
      "email_id": "26",
      "to": "thomas.martin@enron.com, mike.grigsby@enron.com, keith.holst@enron.com, jay.reitmeyer@enron.com, frank.ermis@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Wow",
      "timestamp": "Wed, 6 Sep 2000 04:46:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "007",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "Here sales numbers from Reagan: As you can see his units sold at a variety of prices per square foot. The 1308/1308 model seems to have the most data and looks most similiar to the units you are selling. At 2.7 MM, my bid is .70/sf higher than his units under construction. I am having a hard time justifying paying much more with competition on the way. The price I am bidding is higher than any deals actually done to date.",
    "source": {
      "email_id": "27",
      "to": "cbpres@austin.rr.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 19 Sep 2000 07:26:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "008",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "I will follow up with an email and phone call about Cherry Creek. I am sure Deborah Yates let you know that the bid was rejected on the De Ville property.",
    "source": {
      "email_id": "27",
      "to": "cbpres@austin.rr.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 19 Sep 2000 07:26:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "009",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "What is up with Burnet?",
    "source": {
      "email_id": "28",
      "to": "jsmith@austintx.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 19 Sep 2000 03:15:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "010",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "I need to see the site plan for Burnet. Remember I must get written approval from Brenda Key Stone before I can sell this property and she has concerns about the way the property will be subdivided. I would also like to review the closing statements as soon as possible.",
    "source": {
      "email_id": "29",
      "to": "jsmith@austintx.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: burnet",
      "timestamp": "Mon, 18 Sep 2000 02:34:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "008",
    "domain": "Operational",
    "subdomain": "System Operations",
    "text": "I want to have an accurate rent roll as soon as possible. I faxed you a copy of this file. You can fill in on the computer or just write in the correct amounts and I will input.",
    "source": {
      "email_id": "30",
      "to": "stagecoachmama@hotmail.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Wed, 13 Sep 2000 06:02:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "011",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "I checked my records and I mailed check #1178 for the normal amount on August 28th. I mailed it to 4303 Pate Rd. #29, College Station, TX 77845. I will go ahead and mail you another check. If the first one shows up you can treat the 2nd as payment for October.",
    "source": {
      "email_id": "31",
      "to": "bs_stone@yahoo.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: Sept 1 Payment",
      "timestamp": "Tue, 12 Sep 2000 06:42:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "012",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "I know your concerns about the site plan. I will not proceed without getting the details and getting your approval. I will find that amortization schedule and send it soon.",
    "source": {
      "email_id": "31",
      "to": "bs_stone@yahoo.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Re: Sept 1 Payment",
      "timestamp": "Tue, 12 Sep 2000 06:42:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Financial",
    "subdomain": "Accounting",
    "text": "You wrote fewer checks this month. Spent more money on Materials and less on Labor. June July August Total Materials 2929 4085 4801 Services 53 581 464 Labor 3187 3428 2770",
    "source": {
      "email_id": "32",
      "to": "stagecoachmama@hotmail.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 12 Sep 2000 06:06:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Financial",
    "subdomain": "Accounting",
    "text": "Here are my questions on the August bank statement (attached): 1. Check 1406 Walmart Description and unit? 2. Check 1410 Crumps Detail description and unit? 3. Check 1411 Lucy What is this? 4. Check 1415 Papes Detail description and units? 5. Checks 1416, 1417, and 1425 Why overtime? 6. Check 1428 Ralph's What unit? 7. Check 1438 Walmart? Description and unit? Try and pull together the support for these items and get back to me.",
    "source": {
      "email_id": "32",
      "to": "stagecoachmama@hotmail.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "",
      "timestamp": "Tue, 12 Sep 2000 06:06:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "003",
    "domain": "Operational",
    "subdomain": "Org-Structure Metadata",
    "text": "Attached is the list. Have your people fill in the columns highlighted in yellow. As best can we will try not to overlap on accounts.",
    "source": {
      "email_id": "33",
      "to": "paul.lucci@enron.com, kenneth.shulklapper@enron.com",
      "cc": "",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Contact list for mid market",
      "timestamp": "Tue, 12 Sep 2000 04:23:00 -0700 (PDT)"
    }
  },
    {
    "chunk_id": "014",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "LAND OWNERSHIP & LOANS The property would be purchased in the name of the limited partnership and any land loans, land improvements loans and construction loans would be in the name of the limited partnership. Each of the individual investors and all of the principals in Creekside would also personally guarantee the loans. If the investor(s) do not sign on the loans, this generally means that a larger amount of cash is required and the investor's share of profits is reduced.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "015",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "All loans for residential construction, that are intended for re-sale, are full recourse loans. If we are pursuing multifamily rental developments, the construction loans are still full recourse but the mortgage can often be non-recourse.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "016",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "USE OF INITIAL INVESTMENT The initial investment is used for land deposit, engineering & architectural design, soils tests, surveys, filing fees, legal fees for organization and condominium association formation, and appraisals. Unlike many real estate investment programs, none of the funds are used for fees to Creekside Builders, LLC. These professional expenses will be incurred over the estimated 6 month design and approval period.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "017",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "EARLY LAND COSTS The $4,000 per month costs listed in the cash flow as part of land cost represent the extension fees due to the seller for up to 4 months of extensions on closing. As an alternative, we can close into a land loan at probably 70% of appraised value. With a land value equal to the purchase price of $680,000 this would mean a land loan of $476,000 with estimated monthly interest payments of $3,966, given a 10% annual interest rate, plus approximately 1.25% of the loan amount for closing costs and loan fees.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "018",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "EQUITY AT IMPROVEMENT LOAN Once the site plan is approved by the City of Austin, the City will require the development entity to post funds for fiscal improvements, referred to as the fiscals. This cost represents a bond for the completion of improvements that COA considers vital and these funds are released once the improvements have been completed and accepted by COA. This release will be for 90% of the cost with the remaining 10% released one year after completion.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "019",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "The lot improvement loan is typically 75% of the appraised value of a finished lot, which I suspect will be at least $20,000 and potentially as high as $25,000. This would produce a loan amount of $15,000 on $20,000 per lot. With estimated per lot improvement costs of $9,000, 'fiscals' at $2,000 and the land cost at $8,000, total improved lot cost is $19,000 which means $0 to $4,000 per lot in total equity.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "020",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "Phasing works as follows. If the first phase was say 40 units, the total lot improvement cost might average $31,000 per lot. Of this, probably $13,000 would be for improvements and $19,000 for the land cost. The land loan for undeveloped lots would be 70% of the appraised raw lot value, which I would estimate as $10,000 per lot for a loan value of $7,000 per lot. Then the loan value for each improved lot would be $15,000 per lot. This would give you a total loan of $992,000, total cost of $1,232,645 for equity required of $241,000.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "021",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "CONSTRUCTION LOANS There are three types of construction loans. First, is a speculative (spec) loan that is taken out prior to any pre-sales activity. Second, is a construction loan for a pre-sold unit, but the loan remains in the builder/developers name. Third, is a pre-sold unit with the construction loan in the name of the buyer. We expect to have up to 8 spec loans to start the project and expect all other loans to be pre-sold units with loans in the name of the builder/developer.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "022",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "Spec loans will be for 70% to 75% of value and construction loans for pre-sold units, if the construction loan is from the mortgage lender, will be from 80% to 95% of value.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "023",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "DISBURSEMENTS Disbursements will be handled by the General Partner to cover current and near term third party costs, then to necessary reserves, then to priority payments and then to the partners per the agreement. The General Partner will contract with Creekside Builders, LLC to construct the units and the fee to CB will include a construction management and overhead fee equal to 15% of the direct hard cost excluding land, financing and sales costs.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "024",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "These fees are the only monies to Creekside, Larry Lewter or myself prior to calculation of profit, except for a) direct reimbursement for partnership expenses and b) direct payment to CB for any subcontractor costs that it has to perform. For example, if CB cannot find a good trim carpenter sub, or cannot find enough trim carpenters, etc., and it decides to undertake this function, it will charge the partnership the same fee it was able to obtain from third parties and will disclose those cases to the partnership.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "025",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "Finally, CB will receive a fee for the use of any of its equipment if it is used in lieu of leasing equipment from others. At present CB does not own any significant equipment, but it is considering the purchase of a sky track to facilitate and speed up framing, cornice, roofing and drywall spreading.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "026",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "REPORTING We are more than willing to provide reports to track expenses vs. plan. What did you have in mind? I would like to use some form of internet based reporting.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "027",
    "domain": "Financial",
    "subdomain": "Company Financial Strategy",
    "text": "INVESTOR INPUT We are glad to have the investor's input on design and materials. As always the question will be who has final say if there is disagreement, but in my experience I have always been able to reach consensus. As you, and I presume Keith, want to be involved to learn as much as possible we would make every effort to be accommodating.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "001",
    "domain": "Vendor",
    "subdomain": "Vendor Metadata",
    "text": "CREEKSIDE PROCEEDURES CB procedures for dealing with subs, vendors and professionals is not as formal as your question indicates. In the EXTREMELY tight labor market obtaining 3 bids for each labor trade is not feasible. For the professional subs we use those with whom we have developed a previous rapport. Finally, for vendors they are constantly shopped.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
  {
    "chunk_id": "002",
    "domain": "Vendor",
    "subdomain": "Vendor Metadata",
    "text": "PRE-SELECTED PROFESSIONALS, SUBS AND VENDORS Yes there are many different subs that have been identified and I can provide these if you are interested.",
    "source": {
      "email_id": "34",
      "to": "kholst@enron.com",
      "cc": "Larry Lewter, Claudia L. Crocker",
      "bcc": "",
      "from": "phillip.allen@enron.com",
      "subject": "Investment Structure",
      "timestamp": "Tue, 26 Sep 2000 09:28:00 -0700 (PDT)"
    }
  },
]