import os
import shutil
from collections import defaultdict

def get_organization_plan(directory, separator='-'):
    """Get organization plan without executing it"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Group files by prefix category
    categories = defaultdict(list)
    for file in files:
        # Use configurable separator
        if separator in file:
            prefix = file.split(separator, 1)[0].strip()
        else:
            prefix = "NO_SEPARATOR"
        categories[prefix].append(file)
    
    return categories

def execute_organization(directory, categories, remove_prefix=False, separator='-'):
    """Execute file organization with optional prefix removal"""
    moved_count = 0
    errors = []
    
    for category, files in categories.items():
        category_dir = os.path.join(directory, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        for file in files:
            src = os.path.join(directory, file)
            
            # Determine destination filename
            if remove_prefix and separator in file:
                # Remove prefix and separator
                new_name = file.split(separator, 1)[1].strip()
                # Handle empty filenames
                if not new_name:
                    errors.append(f"'{file}' - Ön ek kaldırıldıktan sonra dosya adı kalmadı")
                    new_name = file
            else:
                new_name = file
                
            dst = os.path.join(category_dir, new_name)
            
            try:
                # Check for name conflicts
                if os.path.exists(dst):
                    errors.append(f"'{file}' -> '{new_name}' - Hedef dosya zaten var")
                    continue
                    
                shutil.move(src, dst)
                moved_count += 1
            except Exception as e:
                errors.append(f"'{file}' taşınırken hata: {str(e)}")
    
    return moved_count, len(categories), errors

if __name__ == "__main__":
    target_dir = input("Enter directory path to organize: ").strip()
    if os.path.isdir(target_dir):
        separator = input("Enter file name separator (default is '-'): ").strip() or '-'
        categories = get_organization_plan(target_dir, separator)
        
        # Show organization plan
        print("\nOrganization Plan:")
        print("=" * 40)
        for category, files in categories.items():
            print(f"\nCategory: {category} (Directory: {category}/)")
            print(f"Files to move: {len(files)}")
            if len(files) > 5:
                print("  " + "\n  ".join(files[:3]) + f"\n  ...and {len(files)-3} more")
            else:
                print("  " + "\n  ".join(files))
        print("=" * 40)
        
        # Get user confirmation
        response = input("\nProceed with organization? (y/n): ").lower()
        if response != 'y':
            print("Operation cancelled.")
        else:
            remove_prefix = input("Remove file name prefixes? (y/n): ").lower() == 'y'
            moved_count, num_categories, errors = execute_organization(target_dir, categories, remove_prefix, separator)
            
            # Show summary
            print(f"\nSuccessfully moved {moved_count} files to {num_categories} directories")
            if errors:
                print("Errors:")
                for error in errors:
                    print(f" - {error}")
            print("Organization complete!")
    else:
        print("Error: Invalid directory path")