import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { BoardService, modType } from '../services/board.service';
import { oponentType } from '../services/board.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  @Output() newItemEvent = new EventEmitter<void>();

  oponents = [oponentType.Player, oponentType.AI];
  mods = [modType.easy, modType.medium, modType.hard];

  constructor(public boardService : BoardService) { }

  goToGame(){
    this.boardService.createArrays();
    console.log(this.boardService.selectedMod + " " + this.boardService.selectedOponent);
    this.newItemEvent.emit();
  }

}
