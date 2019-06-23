# -*- coding: utf-8 -*-
import random

class Deck:
    
    def __init__(self):
        cardNumber = 'A23456789TJQK' #All the numbers
        cardSuit = 'HDSC' #All the suits
        self.deck = [i+j for i in cardNumber for j in cardSuit] #get combinations
        self.count = 0
        
    def drawCard(self): #for now assuming infinite deck size
        return random.sample(self.deck,1)[0] #return as a set not a list
    
    def drawOrderedCard(self):
        cardPulled = self.deck[self.count*4] #suit doesnt matter
        if self.count > len(self.deck)/4:
            self.count=0
        return [cardPulled]

class Players(Deck):
    
    def __init__(self):
        super().__init__()
        self.hand = []
    def hit(self):
        self.hand.append(self.drawCard())
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
    def __init__(self,showSteps = False,defaultHand = True):
        if defaultHand:
            super().__init__()
        else:
            super().__init__()
            self.count=0
            self.hand=[]
        self.showSteps = showSteps
    def setHand(self):
        #the first card is not random but the second card will be
        self.hit()
        
        
    def play(self):
        notBust = True
        stopHitting = False
        while notBust and not stopHitting:
            if super().handTotal() >= 17 or super().handTotal()==21:
                stopHitting = True
            else:
                self.hit()
                if self.showSteps:
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
            if super().handTotal() >= self.whereToStop or super().handTotal()==21:
                stopHitting = True
            else:
                self.hit()
            if super().handTotal() > 21:
                notBust = False
        return super().handTotal()
    
class Simulation():
    def __init__(self,isSimulation,whereToStop,dealerFirstCard,advancedSimulation = False):
        self.isSimulation = isSimulation
        self.whereToStop = whereToStop
        self.advancedSimulation = advancedSimulation
        self.dealerFirstCard = dealerFirstCard
        
    def newHand(self):
        if self.isSimulation and not self.advancedSimulation:
            self.dealer = Dealer()
        elif self.isSimulation and self.advancedSimulation:
            self.dealer = Dealer(defaultHand = False)
            self.dealer.hand = self.dealerFirstCard
            self.dealer.setHand()
        else:
            self.dealer = Dealer(showSteps = True)
                
        self.me = Player(self.whereToStop)
        for i in range(2):
            #dont need to add to dealer hand - i think
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

def plotResults(cardVisible,cardNumber,percentages):
    import matplotlib.pyplot as plt

    plt.imshow(percentages,aspect='equal',origin='lower',extent = [1,13,1,21])
    xticks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    yticks = [i for i in range(1,22)]
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13],xticks)
    plt.yticks([i for i in range(1,22)],yticks)
    plt.xlabel('Dealer Card')
    plt.ylabel('Card to Stop')
    cbar = plt.colorbar() 
    cbar.set_label('Percent Chance to Win',size=18)
    plt.show

                
                
if __name__ == '__main__':
    checkFormat = True
    while checkFormat:
        isSimulation = input('Is this a simulation? ')
        if (isSimulation!='True') and (isSimulation != 'False'):
            print('Please provide a boolean: True or False')
        else:
            checkFormat = False
            isSimulation = bool(isSimulation=='True')
            
    if not isSimulation:
        simulation = Simulation(isSimulation,17)
        keepPlaying = True
        while keepPlaying:
            simulation.newHand()
            simulation.playGame()
            keepPlaying = input('Keep playing?\n')
            checkFormat = True
            while checkFormat:
                if (keepPlaying!='True') and (keepPlaying != 'False'):
                    print('Please provide a boolean: True or False')
                else:
                    checkFormat = False
                    keepPlaying = bool(keepPlaying=='True')
    else:
        deck = Deck()
        percentages = []
        cardNumber = []
        cardVisible = []
        for cards in range(1,22):
            for cardShowing in range(13):
                outcome = []
                for i in range(int(1e2)):
                    #simulation needs as an input the card to use for the dealer!!!
                    simulation = Simulation(isSimulation,cards,deck.drawOrderedCard(),advancedSimulation = True)
                    simulation.newHand()
                    outcome.append(simulation.playGame())
                deck.count+=1
                cardVisible.append(simulation.dealer.hand[0])
                percentages.append(sum(outcome)/len(outcome))
                cardNumber.append(cards)
            deck.count = 0
        cardVisible = [cardVisible[i:i+13] for i in range(0,len(cardVisible),13)]
        cardNumber = [cardNumber[i:i+13] for i in range(0,len(cardNumber),13)]
        percentages = [percentages[i:i+13] for i in range(0,len(percentages),13)]
        plotResults(cardVisible,cardNumber,percentages)
        
    
