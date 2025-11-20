import { defineStore } from 'pinia'

export const useKarteikartenStore = defineStore('karteikarten', {
  state: () => ({
    cards: []
  }),
  actions: {
    addCard(card) {
      this.cards.push(card)
    }
  }
})
