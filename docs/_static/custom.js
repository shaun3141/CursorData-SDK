/* Move navigation links from sidebar header to Section Navigation */
(function() {
    function moveNavigationLinks() {
        // Find the navigation links in the sidebar header
        const sidebarHeaderNav = document.querySelector('.sidebar-header-items__center nav');
        const sectionNavContainer = document.querySelector('.bd-docs-nav .bd-toc-item.navbar-nav');
        
        if (sidebarHeaderNav && sectionNavContainer) {
            // Get the ul element from the navigation
            const navList = sidebarHeaderNav.querySelector('ul.bd-navbar-elements');
            
            if (navList) {
                // Clear the Section Navigation container and add the navigation list
                sectionNavContainer.innerHTML = '';
                sectionNavContainer.appendChild(navList.cloneNode(true));
                
                // Hide the original navigation in sidebar header
                sidebarHeaderNav.style.display = 'none';
            }
        }
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', moveNavigationLinks);
    } else {
        moveNavigationLinks();
    }
    
    // Also run after a short delay to ensure theme has initialized
    setTimeout(moveNavigationLinks, 100);
    setTimeout(moveNavigationLinks, 500);
})();

