![LearnQuickBanner3](https://user-images.githubusercontent.com/85064536/131658944-b76d3550-a437-44d0-9892-ba7ccd3f61af.jpg)


**LearnQuick** is a flashcard application that you can create your own deck, add cards into deck and study.

The main function of LearnQuick is to help the user memorize things. User will create the cards with the sides front and back. Front side will be the question, and back side will be the answer. After the desired number of cards, a deck is completed, for example: Physics deck. While studying deck, cards will be shown one by one and user has to guess the back side, the answer, and rate the difficulty of the card. The frequency of how often which cards will be shown to user is determined by the difficulty rating of the cards. More difficult cards will be shown more often and vice versa.


![LQ](https://user-images.githubusercontent.com/85064536/131725543-a89bb873-e2f8-4c0b-a5e7-3928c698ace7.gif)


![LearnQuickBanner4](https://user-images.githubusercontent.com/85064536/131624607-5ef66562-a032-4f09-80f8-62255529e1bd.jpg)

★ **Method one** : You can [CLICK HERE](https://github.com/mehmetguduk/LearnQuick/releases/tag/Exe) for exe version of application.

★ **Method two** : You can download all py files (MAIN.py, database_functions.py, default_deck.py, images.py, interface.py, requirements.txt) in same folder and convert MAIN.py to exe with any py to exe converter. Then you can run that exe to get access. 

★ **Method three** : You can download all py files (MAIN.py, database_functions.py, default_deck.py, images.py, interface.py, requirements.txt) in same folder and run MAIN.py. 

In order to choose Method two or Method three you should install required modules that project use with the command below.

```pip install -r requirements.txt```

## Requirements

● Windows operating system

● Python 3

● Python pip

● Python Module : PyQt5==5.15.4 


![LearnQuickFeaturesofApplication](https://user-images.githubusercontent.com/85064536/131647525-4150c61d-7f3b-42c6-9da9-422ebcc3925c.jpg)


## Home

● You can reach the GitHub page of the application with the link “Click here for more info about how LearnQuick works”. 

● You can reach the window where you can send me an email with the link “Click here and send me an email”. These emails are very precious to me for improving the application.


## Deck and Cards

●	“Create deck”, “Rename deck”, “Delete deck” buttons work by referring to the text in the box that says “Type deck name here” by default. You can change this text by typing or by choosing a deck from the deck list above. 

●	With the “Sort decks”button, you can sort the decks in the deck list from A to Z. In this way, you can easily find the deck you want in cases where there are too many decks in the list.

●	You can select a deck from the deck list above and then you will be able to see the cards of that selected deck in the card list below. If there is no card in the selected deck, you can click on the "Create card" button to reach the "Card Creation" page where you can add new cards to the deck.

●	While the cards are shown in the card list below; If you select a card and click “Delete card”button, it will delete the selected card from deck.

●	If you click on the 'Front' or 'Back' headers at the top of the card list, you can sort the cards from A to Z.

● You can edit the card by double-clicking any card in the card list.


## Card Creation

●	If you fill two boxes called "Front" and "Back" above and click the 'Add the card below' button, you can send your card to the list below, which will store the cards you have prepared. 

●	The "Clear" button clears card under preparation, in other words clears "Front" and "Back" boxes.

●	You can edit the card by double-clicking on any card you want to change on the list below, which stores the cards you have created. 

●	You can send all created cards in the list to your deck with the "Add all to the deck" button.

●	If you click the "Remove card" button while a card is selected from list, that selected card will be deleted.

●	You can cancel the card adding process by clicking the "Cancel" button.


## Study

●	You can start studying by selecting your deck from the drop-down menu and clicking the 'Start' button. During the study, while you are shown the front of the cards, you are expected to guess the back of the card. After making your guess, click the 'Show' button and compare your guess with the answer.

●	You should rate your guess by clicking the red, orange, yellow, green or blue buttons. The cards you mark as Red have a 35% chance, the cards you mark as Orange have a 25% chance, the cards you mark as Yellow have a 20% chance, the cards you mark as Green have a 15% chance, and the cards you mark as Blue have a 5% chance. Those chances are effecting the cards to get on the screen.  Therefore, you can make sure that the cards that you fell more difficult to guess will appear more often if you rate the card bad by marking. (or vice versa)

●	The counters located below the color buttons contain numbers indicating how many cards you have in the corresponding color.

●	In the bar below the deck selection box, you can see a progress bar with the ratio of how many blue cards are in your deck. Your goal will be to study until all the cards are blue. so you can see what percentage of the deck is complete here.

●	You can stop your studying by clicking the "Stop" button.


## Statistics

●	With the box above where you can select the date, you can see the study you have done on the selected date. 

●	By clicking the "Clear day" button, you can delete all the studies you have done on the selected day, and by clicking the "Remove log" button, you can delete a selected study from the list.

●	By selecting a deck from the drop-down menu, you will be able to see; the number of red, orange, yellow, green, blue or total cards and total studied time, last studied time. (for selected deck)

●	With the "Sort decks" button, you can sort the deck names in the drop-down menu from A to Z.
