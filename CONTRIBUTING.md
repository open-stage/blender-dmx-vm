## Test Scenarios

- Search Versions
- Search Versions with "Include Branches on Search" enabled
- Search Versions should not break when list shrinks and selected is beyond new length
- Download Version should work
- Download Version should be disabled for installed non-branch versions
- Update Version should show for installed branch versions
- Update Version should work
- Update Version should reload version if it's active
- Remove Version should be disabled for non installed versions
- Remove Version should work
- Version should appear as "installed" when it's zip is present on "versions" folder
- Version should appear as "active" when it's the one in use
- Branch Version should appear as "active" when it's the one in use
- Use Version should change current Version
- Use Version should backup and restore profiles
- Use Version should support hot-reload in most scenarios (this one is tricky, don't worry too much)