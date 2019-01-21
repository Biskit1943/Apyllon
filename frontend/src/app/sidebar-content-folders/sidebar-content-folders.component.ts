import { Component, Input, OnInit } from '@angular/core';
import { AlertService, PlayerService } from '../_services';
import { User } from "../_models";
import { first } from "rxjs/operators";

@Component({
  selector: 'app-sidebar-content-folders',
  templateUrl: './sidebar-content-folders.component.html',
  styleUrls: ['./sidebar-content-folders.component.css']
})
export class SidebarContentFoldersComponent implements OnInit {

  songs: any = [];
  @Input() currentUser: User;

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

  addSongToPlaylist(song) {
    const type = 'file';
    const path = song.path + '/' + song.filename;
    this.player.addSongToPlaylist(this.currentUser.username, path, type)
      .pipe(first())
      .subscribe(data => {
        console.log(data);
      }, error => {
        this.alertService.error(error);
        console.log(error);
      });
  }
}
