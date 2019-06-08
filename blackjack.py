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
        for i in self.hand:
            if i[0] in 'TJQK': sum +=10
            elif i[0] == 'A': sum = sum;hasAce = True
            else:             sum += int(i[0])
        if hasAce:
            sum = self.manageAces(sum)
        return sum
        
    def manageAces(self,sum):
        numberOfAces = 0
        for i in self.hand:
            if i[0]=='A':
                numberOfAces+=1
        difference = 21 - sum
        
        if difference < 11:
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
    def __init__(self,whereToStop):
        super().__init__()
        self.whereToStop = whereToStop
        
    def play(self):
        notBust = True
        stopHitting = False
        while notBust and not stopHitting:
            if super().handTotal() >= self.whereToStop:
                stopHitting = True
            else:
                self.hit()
            if super().handTotal() > 21:
                notBust = False
        return super().handTotal()
    
class Simulation():
    def __init__(self,isSimulation,whereToStop):
        self.isSimulation = isSimulation
        self.whereToStop = whereToStop
        
    def newHand(self):
        self.dealer = Dealer()
        self.me = Player(self.whereToStop)
        for i in range(2):
            self.dealer.hit()
            self.me.hit()
            
    def playGame(self):
        if self.isSimulation:
            playerHandCount = self.me.play()
            if playerHandCount >21:
                return False 
            dealerHandCount = self.dealer.play()
            if dealerHandCount>21 or playerHandCount >= dealerHandCount:
                return True
            else:
                return False
        elif not self.isSimulation:
            notBust = True
            playerStops = False
            print('The card you can see is: ',self.dealer.hand[1])
            while notBust and not playerStops:
                print('Your current hand is ',self.me.hand,'\nWith total value: ',self.me.handTotal())
                playerHit = input('Would you like to hit? ')
                if playerHit != 'True' and playerHit != 'False':
                    print('Please provide a boolean: True or False')
                playerHit = bool(playerHit =='True')
                if playerHit:
                    self.me.hit()
                else:
                    playerStops = True
                if self.me.handTotal()>21:
                    notBust = False
                    print('Sorry but you went bust: ',self.me.hand)
            if notBust:
                 dealerFinalHandCount = self.dealer.play()
                 if dealerFinalHandCount >21 or dealerFinalHandCount <= self.me.handTotal():
                     print('You Win!')
                 else:
                     print('You Lose!')

                
                
if __name__ == '__main__':
    checkFormat = True
    while checkFormat:
        isSimulation = input('Is this a simulation? ')
        if (isSimulation!='True') and (isSimulation != 'False'):
            print('Please provide a boolean: True or False')
        else:
            checkFormat = False
            isSimulation = bool(isSimulation=='True')
            
    simulation = Simulation(isSimulation,17)
    keepPlaying = True
    while keepPlaying:
        simulation.newHand()
        simulation.playGame()
        keepPlaying = input('Keep playing?')
        checkFormat = True
        while checkFormat:
            if (keepPlaying!='True') and (keepPlaying != 'False'):
                print('Please provide a boolean: True or False')
            else:
                checkFormat = False
                keepPlaying = bool(keepPlaying=='True')

