import { Component, OnInit, inject } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DataService } from '../../services/data.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  private dataService = inject(DataService);
  private router = inject(Router);
  private authService = inject(AuthService);

  destinos: any[] = [];
  searchData = {
    origin: '1',
    destination: '',
    date: ''
  };

  ngOnInit() {
    this.checkRedirect();
    this.loadDestinos();
  }

  checkRedirect() {
    const user = this.authService.getCurrentUser();
    if (user) {
      switch (user.idTipoUsuario) {
        case 3: this.router.navigate(['/admin']); break;
        case 2: this.router.navigate(['/company']); break;
        case 4: this.router.navigate(['/driver']); break;
      }
    }
  }

  loadDestinos() {
    this.dataService.getDestinos().subscribe({
      next: (data) => {
        this.destinos = data;
      },
      error: (err) => console.error('Error loading destinations', err)
    });
  }

  searchBus() {
    if (this.searchData.destination) {
      this.router.navigate(['/trips'], { queryParams: { idDestino: this.searchData.destination } });
    } else {
      this.router.navigate(['/trips']);
    }
  }
}
