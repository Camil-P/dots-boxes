import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  check : boolean = false;
  title = 'dots-boxes';

  changeCheck(){
    this.check = !this.check;
  }
}
