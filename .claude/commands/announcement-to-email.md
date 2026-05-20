Convert the Cognitivebotics weekly announcement markdown file into a branded HTML email.

Steps:
1. Identify the target file:
   - If $ARGUMENTS specifies a path, use that file.
   - Otherwise, find the most recently dated file matching `*-weekly-announcement.md`
     in `products/cognitivebotics/release-announcements/announcement/`.
2. Run the converter:
     python3 tools/cb_html_email.py <path-to-md-file>
   This saves a `.html` file in the same folder with the same base name.
3. Confirm to the user: state the output filename and note that it is ready to open
   in a browser and paste into Gmail or Outlook.

Rules:
- Never edit the markdown source file — the script is read-only with respect to it.
- If the script errors, show the full error output and do not attempt to fix the HTML by hand.
- The output file always uses the `.html` extension and lives in the same folder as the `.md` source.
