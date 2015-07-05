+ `git pull --rebase` always
+ `git checkout -b feature/my-awesome-feature` before committing anything
+ `git commit --amend` whenever possible
+ `git commit --fixup` and `git commit --squash` in case you pushed to origin and you don't want to force push now
+ Write long and meaningful commit messages
+ Create a Pull Request and continue pushing more commits till review is accepted
+ `git rebase -i --autosquash master feature/my-awesome-feature` and squash all unwanted commits
+ `git push --force-with-lease origin my-awesome-feature` when branches have diverged
+ Merge the Pull Request
