# -*- coding: utf-8 -*-
import random

class Deck:
    
    def __init__(self):
        cardNumber = 'A23456789TJQK' #All the numbers
        cardSuit = 'HDSC' #All the suits
        self.deck = {i+j for i in cardNumber for j in cardSuit} #get combinations
        
    def drawCard(self): #for now assuming infinite deck size
        return random.sample(self.deck,1)[0] #return as a set not a list

class Players(Deck):
    
    def __init__(self):
        super().__init__()
        self.hand = []
    def hit(self):
        self.hand.append(super().drawCard())
    def handTotal(self):
        sum = 0
        hasAce = False
        if 'A' in self.hand:
            hasAce = True
        for i in self.hand:
            if i[0] in 'TJQK': sum +=10
            elif i[0] == 'A': sum = sum
            else:             sum += int(i[0])
        if hasAce:
            sum = self.manageAces(sum)
        return sum
        
    def manageAces(self,sum):
        numberOfAces = 0
        for i in self.hand:
            if self.hand[i][0]=='A':
                numberOfAces+=1
        difference = 21 - sum
        
        if difference <= 11:
            sum += numberOfAces
        else:
            sum += (numberOfAces-1) + 11
        return sum
        
class Dealer(Players):
    def __init__(self):
        super().__init__()
        
    def play(self):
        notBust = True
        stopHitting = False
        while notBust and not stopHitting:
            if super().handTotal() >= 17:
                stopHitting = True
            else:
                self.hit()
                print('The dealer hits')
                print("The dealer's hand now: ",self.hand)
            if super().handTotal() > 21:
                notBust = False
        return super().handTotal()

class Player(Players):
    def __init__(self):
        super().__init__()
        
    def shouldHit(self):
        if not self.hand :
            return True
        if self.handTotal()<20:
            return True
        else:
            return False
        
        
if __name__ == '__main__':
    #initialize dealer and current player
    dealer = Dealer()
    me = Player()

    #initialize 2 cards for players and dealer
    for i in range(2):
        dealer.hit()
        me.hit()
    
    #checking if doing comp study or playing
    checkFormat = True
    while checkFormat:
        isSimulation = input('Is this a simulation? ')
        if (isSimulation!='True') and (isSimulation != 'False'):
            print('Please provide a boolean: True or False')
        else:
            checkFormat = False
            isSimulation = bool(isSimulation=='True')
    
    #for game loop
    notBust = True 
    playerStops = False     
    if not isSimulation:
        print('The card you can see is: ',dealer.hand[1])
        while notBust and not playerStops:
            print('Your current hand is ',me.hand,'\nWith total value: ',me.handTotal())
            playerHit = input('Would you like to hit? ')
            if playerHit != 'True' and playerHit != 'False':
                print('Please provide a boolean: True or False')
            playerHit = bool(playerHit =='True')
            if playerHit:
                me.hit()
            else:
                playerStops = True
            if me.handTotal()>21:
                notBust = False
                print('Sorry but you went bust: ',me.hand)
        if notBust:
            print('The dealer hand is: ',dealer.hand)
            dealerFinalHandCount = dealer.play()
            if dealerFinalHandCount >21 or dealerFinalHandCount < me.handTotal():
                print('You Win!')
            else:
                print('You Lose!')
            

