import { Version } from '@microsoft/sp-core-library';
import { IPropertyPaneConfiguration, PropertyPaneTextField } from '@microsoft/sp-property-pane';
import { BaseClientSideWebPart } from '@microsoft/sp-webpart-base';
import { SPHttpClient, SPHttpClientResponse } from '@microsoft/sp-http';

export interface ISopSearchWebPartProps {
  listName: string;
}

export default class SopSearchWebPart extends BaseClientSideWebPart<ISopSearchWebPartProps> {
  private allItems: any[] = [];
  private fieldNames = {
    title: 'Title',
    action: 'field_1',
    tags: 'field_6',
    role: 'field_2'
  };

  public render(): void {
    this.domElement.innerHTML = `
      <style>
        .sop-search-container { font-family: 'Segoe UI', sans-serif; padding: 20px; max-width: 1200px; }
        .sop-header { display: flex; align-items: center; margin-bottom: 20px; }
        .sop-header h2 { margin: 0; color: #323130; }
        .sop-header span:first-child { font-size: 24px; margin-right: 10px; }
        .sop-header span:last-child { margin-left: auto; color: #605e5c; font-size: 14px; }
        .sop-filters { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }
        .sop-filter-group { position: relative; }
        .sop-filter-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #323130; }
        .sop-filter-group input { width: 100%; padding: 8px; border: 1px solid #8a8886; border-radius: 4px; box-sizing: border-box; }
        .sop-suggestions { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #8a8886; border-top: none; border-radius: 0 0 4px 4px; max-height: 200px; overflow-y: auto; z-index: 1000; display: none; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .sop-suggestions.active { display: block; }
        .sop-suggestion { padding: 8px 12px; cursor: pointer; border-bottom: 1px solid #edebe9; }
        .sop-suggestion:hover { background: #f3f2f1; }
        .sop-suggestion:last-child { border-bottom: none; }
        .sop-buttons { margin-bottom: 20px; }
        .sop-btn-search { background: #0078d4; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-right: 10px; }
        .sop-btn-clear { background: white; color: #323130; border: 1px solid #8a8886; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .sop-results table { width: 100%; border-collapse: collapse; }
        .sop-results th { padding: 12px; text-align: left; border-bottom: 2px solid #edebe9; background: #f3f2f1; }
        .sop-results td { padding: 12px; border-bottom: 1px solid #edebe9; }
      </style>
      <div class="sop-search-container">
        <div class="sop-header">
          <span>🔍</span>
          <h2>SOP Activity Search</h2>
          <span>Start typing in any filter to see suggestions, then click Search</span>
        </div>
        <div class="sop-filters">
          <div class="sop-filter-group">
            <label>SOP Title</label>
            <input type="text" id="filterTitle" placeholder="Start typing..." autocomplete="off">
            <div class="sop-suggestions" id="suggestionsTitle"></div>
          </div>
          <div class="sop-filter-group">
            <label>SOP Action</label>
            <input type="text" id="filterAction" placeholder="Start typing..." autocomplete="off">
            <div class="sop-suggestions" id="suggestionsAction"></div>
          </div>
          <div class="sop-filter-group">
            <label>Tags</label>
            <input type="text" id="filterTags" placeholder="Start typing..." autocomplete="off">
            <div class="sop-suggestions" id="suggestionsTags"></div>
          </div>
          <div class="sop-filter-group">
            <label>Responsible Role (RACI)</label>
            <input type="text" id="filterRole" placeholder="Start typing..." autocomplete="off">
            <div class="sop-suggestions" id="suggestionsRole"></div>
          </div>
        </div>
        <div class="sop-buttons">
          <button class="sop-btn-search" id="btnSearch">🔍 Search</button>
          <button class="sop-btn-clear" id="btnClear">✕ Clear</button>
        </div>
        <div class="sop-results" id="resultsContainer">
          <p style="color: #605e5c;">Enter search criteria above and click Search.</p>
        </div>
      </div>
    `;

    this._loadData();
  }

  private _bindEvents(): void {
    const btnSearch = this.domElement.querySelector('#btnSearch');
    const btnClear = this.domElement.querySelector('#btnClear');

    if (btnSearch) btnSearch.addEventListener('click', () => this._search());
    if (btnClear) btnClear.addEventListener('click', () => this._clear());

    this._setupTypeahead('filterTitle', 'suggestionsTitle', this.fieldNames.title);
    this._setupTypeahead('filterAction', 'suggestionsAction', this.fieldNames.action);
    this._setupTypeahead('filterTags', 'suggestionsTags', this.fieldNames.tags);
    this._setupTypeahead('filterRole', 'suggestionsRole', this.fieldNames.role);

    document.addEventListener('click', () => {
      const suggestions = this.domElement.querySelectorAll('.sop-suggestions');
      suggestions.forEach(s => s.classList.remove('active'));
    });
  }

  private _setupTypeahead(inputId: string, suggestionsId: string, field: string): void {
    const input = this.domElement.querySelector(`#${inputId}`) as HTMLInputElement;
    const suggestionsDiv = this.domElement.querySelector(`#${suggestionsId}`) as HTMLElement;

    if (!input || !suggestionsDiv) return;

    input.addEventListener('input', () => {
      const value = input.value.toLowerCase().trim();
      if (value.length < 1) {
        suggestionsDiv.classList.remove('active');
        return;
      }

      const uniqueValues = this._getUniqueValues(field);
      const matches = uniqueValues
        .filter(v => v.toLowerCase().includes(value))
        .slice(0, 10);

      if (matches.length === 0) {
        suggestionsDiv.classList.remove('active');
        return;
      }

      suggestionsDiv.innerHTML = matches.map(m => 
        `<div class="sop-suggestion" data-value="${this._escapeHtml(m)}">${this._escapeHtml(m)}</div>`
      ).join('');
      suggestionsDiv.classList.add('active');

      suggestionsDiv.querySelectorAll('.sop-suggestion').forEach(el => {
        el.addEventListener('mousedown', (e) => {
          e.preventDefault();
          e.stopPropagation();
          input.value = (el as HTMLElement).getAttribute('data-value') || '';
          suggestionsDiv.classList.remove('active');
        });
      });
    });

    input.addEventListener('blur', () => {
      setTimeout(() => suggestionsDiv.classList.remove('active'), 200);
    });

    input.addEventListener('focus', () => {
      if (input.value.length >= 1) {
        input.dispatchEvent(new Event('input'));
      }
    });
  }

  private _escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  private _getUniqueValues(field: string): string[] {
    const values = new Set<string>();
    this.allItems.forEach(item => {
      const val = item[field];
      if (val && typeof val === 'string' && val.trim()) {
        values.add(val.trim());
      }
    });
    return Array.from(values).sort();
  }

  private _loadData(): void {
    const listName = this.properties.listName || 'Key_SOP_Matrix';
    const url = `${this.context.pageContext.web.absoluteUrl}/_api/web/lists/getbytitle('${listName}')/items?$top=5000`;

    this.context.spHttpClient.get(url, SPHttpClient.configurations.v1)
      .then((response: SPHttpClientResponse) => response.json())
      .then((data: any) => {
        this.allItems = data.value || [];
        
        // Log first item to see field values
        if (this.allItems.length > 0) {
          const firstItem = this.allItems[0];
          console.log('First item data:', {
            Title: firstItem.Title,
            field_1: firstItem.field_1,
            field_2: firstItem.field_2,
            field_3: firstItem.field_3,
            field_4: firstItem.field_4,
            field_5: firstItem.field_5,
            field_6: firstItem.field_6,
            Tags: firstItem.Tags,
            Responsible_RACI: firstItem['Responsible_x0028_RACI_x0029_']
          });
        }
        
        this._bindEvents();
      })
      .catch((error: any) => {
        this.domElement.querySelector('#resultsContainer')!.innerHTML = 
          `<p style="color: #a4262c;">Error loading data. Make sure the list "${listName}" exists.</p>`;
      });
  }

  private _search(): void {
    const title = (this.domElement.querySelector('#filterTitle') as HTMLInputElement).value.toLowerCase().trim();
    const action = (this.domElement.querySelector('#filterAction') as HTMLInputElement).value.toLowerCase().trim();
    const tags = (this.domElement.querySelector('#filterTags') as HTMLInputElement).value.toLowerCase().trim();
    const role = (this.domElement.querySelector('#filterRole') as HTMLInputElement).value.toLowerCase().trim();

    if (!title && !action && !tags && !role) {
      this.domElement.querySelector('#resultsContainer')!.innerHTML = 
        '<p style="color: #605e5c;">Please enter at least one search criteria.</p>';
      return;
    }

    const filtered = this.allItems.filter(item => {
      const itemTitle = (item[this.fieldNames.title] || '').toLowerCase();
      const itemAction = (item[this.fieldNames.action] || '').toLowerCase();
      const itemTags = (item[this.fieldNames.tags] || '').toLowerCase();
      const itemRole = (item[this.fieldNames.role] || '').toLowerCase();

      const matchTitle = !title || itemTitle.includes(title);
      const matchAction = !action || itemAction.includes(action);
      const matchTags = !tags || itemTags.includes(tags);
      const matchRole = !role || itemRole.includes(role);

      return matchTitle && matchAction && matchTags && matchRole;
    });

    this._showResults(filtered);
  }

  private _clear(): void {
    (this.domElement.querySelector('#filterTitle') as HTMLInputElement).value = '';
    (this.domElement.querySelector('#filterAction') as HTMLInputElement).value = '';
    (this.domElement.querySelector('#filterTags') as HTMLInputElement).value = '';
    (this.domElement.querySelector('#filterRole') as HTMLInputElement).value = '';
    this.domElement.querySelector('#resultsContainer')!.innerHTML = 
      '<p style="color: #605e5c;">Enter search criteria above and click Search.</p>';
  }

  private _showResults(items: any[]): void {
    const container = this.domElement.querySelector('#resultsContainer')!;
    
    if (items.length === 0) {
      container.innerHTML = '<p style="color: #605e5c;">No results found.</p>';
      return;
    }

    let html = `
      <p style="color: #605e5c; margin-bottom: 10px;">Showing ${items.length} result${items.length !== 1 ? 's' : ''}</p>
      <table>
        <thead>
          <tr>
            <th>SOP Title</th>
            <th>Action</th>
            <th>Tags</th>
            <th>Role (RACI)</th>
          </tr>
        </thead>
        <tbody>
    `;

    items.forEach(item => {
      const title = item[this.fieldNames.title] || '';
      const action = item[this.fieldNames.action] || '';
      const tags = item[this.fieldNames.tags] || '';
      const role = item[this.fieldNames.role] || '';
      
      html += `
        <tr>
          <td>${this._escapeHtml(title)}</td>
          <td>${this._escapeHtml(action)}</td>
          <td>${this._escapeHtml(tags)}</td>
          <td>${this._escapeHtml(role)}</td>
        </tr>
      `;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
  }

  protected get dataVersion(): Version {
    return Version.parse('1.0');
  }

  protected getPropertyPaneConfiguration(): IPropertyPaneConfiguration {
    return {
      pages: [{
        header: { description: 'SOP Search Configuration' },
        groups: [{
          groupName: 'Settings',
          groupFields: [
            PropertyPaneTextField('listName', {
              label: 'SharePoint List Name',
              description: 'Enter the name of your SOP list',
              value: 'Key_SOP_Matrix'
            })
          ]
        }]
      }]
    };
  }
}
