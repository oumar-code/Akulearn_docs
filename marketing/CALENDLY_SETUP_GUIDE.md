# Calendly Setup & Integration Guide

## Quick Setup (5 minutes)

### 1. Create Calendly Account
**Go to**: [calendly.com](https://calendly.com)

**Steps**:
1. Click "Sign Up" (top right)
2. Choose "Free" plan ($0/month)
3. Enter email & create password
4. Verify email address
5. Skip onboarding or complete profile

---

## Create Event Type: "30-Minute AI Consultation"

### Basic Info
| Field | Value |
|-------|-------|
| **Event Title** | 30-Minute AI/NLP Consultation |
| **Description** | Let's discuss your AI/NLP needs and explore how VersaTech can help |
| **Duration** | 30 minutes |
| **Color** | Blue or your brand color |

### Location
- **Option A**: Phone (include your WhatsApp or phone number)
- **Option B**: Google Meet (auto-generated)
- **Option C**: Custom - "I'll send you a Zoom link after booking" |

### Availability
**Recommended Default** (adjust as needed):
```
Monday-Friday: 2:00 PM - 8:00 PM (WAT, Nigeria time)
Saturday-Sunday: Unavailable
Minimum notice: 24 hours
```

**UTC Equivalent**: 1:00 PM - 7:00 PM UTC

### Settings
- [ ] Enable "Multiple event type" (allow back-to-back bookings)
- [ ] Disable "Show available times in my local time zone" (let people see WAT)
- [x] Enable "Send confirmation email to invitees"
- [x] Enable "Send reminder email before the event"

---

## Copy Your Calendly Link

Once event is created:

1. Click your event ("30-Minute AI Consultation")
2. Copy the link: `https://calendly.com/oumar-code/30min-consultation` (example)
3. Share widely

---

## Integration Points (Replace Placeholders)

### 1. personal_portfolio/README.md
**Find**: (search for "Schedule Call")
```markdown
## Let's Connect
📅 **Schedule a consultation**: [Book a 30-minute call](https://calendly.com/oumar-code/30min-consultation)
```

### 2. versatech_profile/README.md
**Find**: "Interested in learning more?"
```markdown
📅 **Schedule VersaTech Consultation**: [Book a 30-minute call](https://calendly.com/oumar-code/30min-consultation)
```

### 3. personal_portfolio/case_studies/akulearn.md
**End of file**: 
```markdown
---
**Want to build something like this for your organization?**  
[Schedule a consultation](https://calendly.com/oumar-code/30min-consultation) to discuss your EdTech or AI needs.
```

### 4. personal_portfolio/case_studies/voice_dataset.md
**End of file**:
```markdown
---
**Need Hausa ASR, multilingual NLP, or low-resource voice solutions?**  
[Schedule a consultation](https://calendly.com/oumar-code/30min-consultation) to explore what's possible.
```

### 5. personal_portfolio/case_studies/geospatial_mapping.md
**End of file**:
```markdown
---
**Interested in geospatial analysis for your region or organization?**  
[Schedule a consultation](https://calendly.com/oumar-code/30min-consultation) to map your opportunities.
```

### 6. personal_portfolio/kaggle/assyrian_translation_baseline.ipynb
**Section 7 footer**:
```markdown
📅 **Schedule Consultation**: [Book a 30-minute call](https://calendly.com/oumar-code/30min-consultation)
```

### 7. marketing/social_posts.md
**All CTA references**:
- Find: "Schedule Consultation: [Add Calendly link here]"
- Replace with: "Schedule Consultation: https://calendly.com/oumar-code/30min-consultation"

### 8. Email signature (Gmail, Outlook)
```
Best regards,
Umar Abubakar
🤖 AI/NLP Engineer | EdTech Pioneer | VersaTech Founder
📧 umarabubakar1960@gmail.com | 📞 +234 814 495 5037
📅 Book a consultation: https://calendly.com/oumar-code/30min-consultation
```

---

## Advanced Customizations (Optional)

### Add Event Details
On your Calendly event, include:
```
Thank you for scheduling! Here's what to expect:

**Before the Call**:
- Share 1-2 sentences about your challenge
- Let me know your timezone

**During the Call** (30 min):
- Understand your needs (10 min)
- Discuss VersaTech capabilities (10 min)
- Next steps (10 min)

**After the Call**:
- You'll receive a summary + next steps email
- I'll send relevant case studies or resources
```

### Set Up Timezone Handling
1. In Calendly settings → **Timezone**: Set to "Africa/Lagos" (WAT)
2. This ensures everyone sees times in your zone

### Add Reminder Sequence
- 1 hour before: SMS/email reminder
- Day before: Follow-up email with context

---

## Tracking Bookings

### Weekly Metrics to Monitor
```
| Metric | Target |
|--------|--------|
| Clicks from LinkedIn | 5-10 |
| Bookings from social | 2-3 |
| Booking → Meeting rate | 80%+ |
| Avg time to book | < 2 days |
| Customer sentiment | 8/10+ satisfaction |
```

### CRM Notes (Manual)
After each call, note:
- Prospect name, company, industry
- Problem discussed
- VersaTech services mentioned
- Follow-up action
- Likely deal value

---

## Email Follow-Up Template

**Subject**: [Your Name] - AI/NLP Consultation Available

```
Hi [Prospect Name],

Thanks for visiting my portfolio! 

I'd love to discuss how VersaTech can help with:
- [Specific challenge from their industry/profile]
- AI/ML strategy and implementation
- Multilingual NLP, voice solutions, or EdTech platforms
- DevOps/MLOps infrastructure

**Available times**:
- Weekdays (Mon-Fri): 2-8 PM Lagos time
- [Share Calendly link]

Looking forward to our conversation!

Best regards,
Umar
---
VersaTech | Custom AI Solutions
📧 umarabubakar1960@gmail.com
📞 +234 814 495 5037
```

---

## Pro Tips

1. **Test Your Link**: Before sharing, click your Calendly link to confirm it works
2. **Time Zone Call-Out**: In all CTAs, mention "Lagos time" or "9 AM - 5 PM UTC"
3. **Buffer Time**: Set 30-min gaps between bookings (travel, prep time)
4. **Confirmation**: Always send a follow-up email 1 hour before call with Zoom/call link
5. **Testimonials**: Ask satisfied customers for LinkedIn recommendations after calls

---

## FAQ

**Q: Why free Calendly vs Pro?**  
A: Free tier is perfect for early-stage founder. Upgrade to Pro ($12/mo) when you have 10+ monthly meetings.

**Q: Can I set different rates for different customers?**  
A: Calendly's free tier doesn't support this. Use a manual booking form for custom pricing.

**Q: How do I handle timezone differences?**  
A: Calendly shows times in invitees' local timezone. Always mention your timezone (Lagos, UTC+1) in description.

**Q: Can I collect payment through Calendly?**  
A: Free tier doesn't support payment. Use Stripe or PayPal for paid consultations (upgrade to Calendly Pro).

**Q: What if I'm overbooked?**  
A: In Calendly settings, set "max hours per day" or manually mark times unavailable.

---

## Deployment Checklist

- [ ] Create Calendly account and event type
- [ ] Copy your Calendly link
- [ ] Update personal_portfolio/README.md with link
- [ ] Update versatech_profile/README.md with link
- [ ] Update all 3 case studies with link
- [ ] Update Kaggle notebook footer with link
- [ ] Update marketing/social_posts.md with link
- [ ] Test link works (click it!)
- [ ] Add to email signature
- [ ] Post first social media post with Calendly CTA
- [ ] Monitor bookings daily for first week

---

**Last Updated**: January 3, 2026  
**Expected Time to Deploy**: 5 minutes setup + 10 minutes link updates = 15 min total
