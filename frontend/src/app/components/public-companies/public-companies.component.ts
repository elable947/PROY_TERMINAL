import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { PublicService } from '../../services/public.service';

@Component({
    selector: 'app-public-companies',
    standalone: true,
    imports: [CommonModule, RouterModule],
    templateUrl: './public-companies.component.html',
    styleUrl: './public-companies.component.css'
})
export class PublicCompaniesComponent implements OnInit {
    private publicService = inject(PublicService);
    companies: any[] = [];
    loading = true;

    ngOnInit() {
        this.publicService.getCompanies().subscribe({
            next: (data) => {
                this.companies = data;
                this.loading = false;
            },
            error: (err) => {
                console.error(err);
                this.loading = false;
            }
        });
    }
}
