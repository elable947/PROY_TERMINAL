import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { PublicService } from '../../services/public.service';
import { AuthService } from '../../services/auth.service';
import { SeatSelectionModalComponent } from '../seat-selection-modal/seat-selection-modal.component';

@Component({
    selector: 'app-public-trips',
    standalone: true,
    imports: [CommonModule, RouterModule, FormsModule, SeatSelectionModalComponent],
    templateUrl: './public-trips.component.html',
    styleUrl: './public-trips.component.css'
})
export class PublicTripsComponent implements OnInit {
    private publicService = inject(PublicService);
    private route = inject(ActivatedRoute);

    trips: any[] = [];
    destinations: any[] = [];
    companies: any[] = [];
    loading = true;

    // Filters
    selectedDest: string = '';
    selectedCompany: string = '';

    ngOnInit() {
        this.loadFilters();

        // Check URL params for initial filters
        this.route.queryParams.subscribe(params => {
            if (params['idEmpresa']) this.selectedCompany = params['idEmpresa'];
            if (params['idDestino']) this.selectedDest = params['idDestino'];
            this.searchTrips();
        });
    }

    loadFilters() {
        this.publicService.getDestinations().subscribe(data => this.destinations = data);
        this.publicService.getCompanies().subscribe(data => this.companies = data);
    }

    searchTrips() {
        this.loading = true;
        const destId = this.selectedDest ? parseInt(this.selectedDest) : undefined;
        const compId = this.selectedCompany ? parseInt(this.selectedCompany) : undefined;

        this.publicService.getPublicTrips(destId, compId).subscribe({
            next: (data) => {
                this.trips = data;
                this.loading = false;
            },
            error: (err) => {
                console.error(err);
                this.loading = false;
            }
        });
    }

    clearFilters() {
        this.selectedDest = '';
        this.selectedCompany = '';
        this.searchTrips();
    }

    // Purchase Logic
    showPurchaseModal = false;
    selectedTripId: number | null = null;
    selectedTrip: any = null; // New property
    private authService = inject(AuthService);
    private router = inject(Router);

    openPurchaseModal(trip: any) {
        if (!this.authService.isLoggedIn()) {
            // Redirect to login
            this.router.navigate(['/login']);
            return;
        }
        this.selectedTripId = trip.idViaje;
        this.selectedTrip = trip; // Store trip
        this.showPurchaseModal = true;
    }

    closePurchaseModal() {
        this.showPurchaseModal = false;
        this.selectedTripId = null;
    }

    onPurchaseSuccess(res: any) {
        // Refresh trips to update availability
        this.searchTrips();
    }
}
