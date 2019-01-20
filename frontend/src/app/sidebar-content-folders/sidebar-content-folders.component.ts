import { Component, OnInit } from '@angular/core';
import { PlayerService, AlertService} from '../_services';

@Component({
  selector: 'app-sidebar-content-folders',
  templateUrl: './sidebar-content-folders.component.html',
  styleUrls: ['./sidebar-content-folders.component.css']
})
export class SidebarContentFoldersComponent implements OnInit {

  songs: Array<string> = [];
  constructor(private player: PlayerService, private alertService: AlertService) {
  }

  ngOnInit() {
    this.player.listSongs().subscribe(songs => {
      console.log(songs);
      this.songs = ['Creme de la Creme - Letzte Nacht', 'Prinz Pi - Elfenbeinturm', 'Papa Roach - Last Resort'];
    }, err => {
      this.alertService.error(err);
    });
  }
}
