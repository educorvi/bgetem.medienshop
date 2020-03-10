# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s bgetem.medienshop -t test_artikel.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src bgetem.medienshop.testing.BGETEM_MEDIENSHOP_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_artikel.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Artikel
  Given a logged-in site administrator
    and an add artikel form
   When I type 'My Artikel' into the title field
    and I submit the form
   Then a artikel with the title 'My Artikel' has been created

Scenario: As a site administrator I can view a Artikel
  Given a logged-in site administrator
    and a artikel 'My Artikel'
   When I go to the artikel view
   Then I can see the artikel title 'My Artikel'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add artikel form
  Go To  ${PLONE_URL}/++add++Artikel

a artikel 'My Artikel'
  Create content  type=Artikel  id=my-artikel  title=My Artikel


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the artikel view
  Go To  ${PLONE_URL}/my-artikel
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a artikel with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the artikel title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
