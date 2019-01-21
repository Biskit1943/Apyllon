import { Component, OnInit } from '@angular/core';
import { PlayerService, AlertService} from '../_services';

@Component({
  selector: 'app-sidebar-content-folders',
  templateUrl: './sidebar-content-folders.component.html',
  styleUrls: ['./sidebar-content-folders.component.css']
})
export class SidebarContentFoldersComponent implements OnInit {

  songs: any = [];
  constructor(private player: PlayerService, private alertService: AlertService) {
  }

  ngOnInit() {
    this.player.listSongs().subscribe(songs => {
      // @ts-ignore
      this.songs = Array.from(songs);
    }, err => {
      this.alertService.error(err);
      this.songs = ['No Songs in database'];
    });
  }
}
