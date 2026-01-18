$word = New-Object -ComObject Word.Application
$word.Visible = $false

$doc = $word.Documents.Open("C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.2.4 Foreman.doc")

$sopBlock = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role is responsible for executing the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover
- Section 1.3: Scope and Contract Review
- Section 1.5: Material Handling Plan
- Section 1.6: Layout and Sequencing Plan
- Section 1.7: Schedule Development and Tracking
- SOP 9.4.631: Release of Large Feeder Wire
- SOP OPS-CO-001: Change Order Management

CRITICAL REQUIREMENTS:
- Per OPS-CO-001/MD 9.3: NEVER perform changed work without PM authorization
- Per Section 1.7/MD 9.3: Document in daily reports any scheduling delays
- Per SOP 9.4.631/MD 9.3: Complete timecards daily with installed quantities

Training Reference: Foreman Training Binder Tabs 2-14, 22, 38, 41, 49, 57
Skill Level: L7 per GSL Academy Target Skill Rules
================================================================================

"@

$find = $doc.Content.Find
$find.ClearFormatting()
$null = $find.Execute("Essential Duties and Responsibilities:")

$range = $doc.Range($find.Parent.End, $find.Parent.End)
$range.InsertAfter($sopBlock)

$doc.SaveAs("C:\Users\tewing\Desktop\Claude Projects\Revised Job Descriptions\Policy Manual 7.2.4 Foreman - REVISED.doc")
$doc.Close()
$word.Quit()

Write-Host "Foreman JD updated successfully"
