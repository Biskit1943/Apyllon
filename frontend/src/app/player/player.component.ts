import { Component, Input } from '@angular/core';
import { AlertService, PlayerService } from '../_services';
import { User } from '../_models';
import { first } from "rxjs/operators";

@Component({
    selector: 'app-player',
    templateUrl: './player.component.html',
    styleUrls: ['./player.component.css']
})
export class PlayerComponent {

    @Input() currentUser: User;
    private isShuffle = false;
    private isLoop = false;
    private currentSong = '';
    private currentArtist = '';
    private nextSong = '';
    private previousSong = '';

    constructor(private player: PlayerService, private alertService: AlertService) {
        this.update();
        setInterval(() => {
            this.update();
        }, 10000);
    }

    previous(event) {
        const state = this.player.prev();
    }

    next(event) {
        const state = this.player.next();
    }

    playPause(event) {
        const state = this.player.playPause();
    }

    shuffle(event) {
        this.player.shuffle(this.currentUser.username)
            .pipe(first())
            .subscribe(data => {
                    this.isShuffle = !this.isShuffle;
                },
                err => {
                    console.log(err);
                    this.alertService.error(err);
                });
    }

    loop(event) {
        this.player.loop(this.currentUser.username)
            .pipe(first())
            .subscribe(data => {
                    this.isLoop = !this.isLoop;
                },
                err => {
                    console.log(err);
                    this.alertService.error(err);
                });
    }

    async shuffled() {
        try {
            this.isShuffle = await this.player.isShuffle();
        } catch (err) {
            console.log(err);
        }
    }

    async looped() {
        try {
            this.isLoop = await this.player.isLoop();
        } catch (err) {
            console.log(err);
        }
    }

    async update() {
        try {
            const state = await this.player.getState();
            if (state && state.hasOwnProperty('shuffle') && state.hasOwnProperty('loop')) {
                console.log(state);
                this.isLoop = state['loop'] === 'true';
                this.isShuffle = state['shuffle'] === 'true';
                this.currentSong = state['current'];
                this.nextSong = state['next'];
                this.previousSong = state['previous'];
            }
        } catch (err) {
            console.log(err);
        }
    }
}
