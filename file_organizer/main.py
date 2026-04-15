"""
Smart File Organizer - Main CLI Entry Point
A professional file management automation tool.
"""
import typer
from pathlib import Path
from typing import Optional
from organizer.mover import FileMover
from organizer.duplicate import DuplicateFinder
from organizer.watcher import FolderWatcher
from organizer.stats import FolderStats
from organizer.renamer import FileRenamer
from organizer.history import OperationHistory
from organizer.config import Config
import logging

app = typer.Typer(help="Smart File Organizer - Automate your file management")
config = Config()
history = OperationHistory()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.command()
def organize(
    path: Path = typer.Argument(..., help="Directory path to organize"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes without moving files")
):
    """Organize files by extension/type."""
    if not path.exists() or not path.is_dir():
        typer.secho(f"Error: {path} is not a valid directory", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"🗂️  Organizing files in: {path}", fg=typer.colors.CYAN)
    mover = FileMover(config)
    result = mover.organize_by_type(path, dry_run=dry_run)
    
    if not dry_run:
        history.save_operation("organize", path, result)
        typer.secho(f"✅ Organized {result['moved']} files successfully!", fg=typer.colors.GREEN)
    else:
        typer.secho(f"🔍 Dry run: Would move {result['moved']} files", fg=typer.colors.YELLOW)


@app.command()
def organize_date(
    path: Path = typer.Argument(..., help="Directory path to organize"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes without moving files")
):
    """Organize files by modified date (YYYY/MM structure)."""
    if not path.exists() or not path.is_dir():
        typer.secho(f"Error: {path} is not a valid directory", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"📅 Organizing files by date in: {path}", fg=typer.colors.CYAN)
    mover = FileMover(config)
    result = mover.organize_by_date(path, dry_run=dry_run)
    
    if not dry_run:
        history.save_operation("organize_date", path, result)
        typer.secho(f"✅ Organized {result['moved']} files by date!", fg=typer.colors.GREEN)
    else:
        typer.secho(f"🔍 Dry run: Would move {result['moved']} files", fg=typer.colors.YELLOW)


@app.command()
def rename(
    path: Path = typer.Argument(..., help="Directory path"),
    prefix: str = typer.Option("file", "--prefix", help="Prefix for renamed files")
):
    """Bulk rename files with custom prefix."""
    if not path.exists() or not path.is_dir():
        typer.secho(f"Error: {path} is not a valid directory", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"✏️  Renaming files in: {path}", fg=typer.colors.CYAN)
    renamer = FileRenamer()
    result = renamer.bulk_rename(path, prefix)
    
    history.save_operation("rename", path, result)
    typer.secho(f"✅ Renamed {result['renamed']} files!", fg=typer.colors.GREEN)


@app.command()
def duplicates(path: Path = typer.Argument(..., help="Directory path to scan")):
    """Find duplicate files using SHA256 hash."""
    if not path.exists() or not path.is_dir():
        typer.secho(f"Error: {path} is not a valid directory", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"🔍 Scanning for duplicates in: {path}", fg=typer.colors.CYAN)
    finder = DuplicateFinder()
    dupes = finder.find_duplicates(path)
    
    if dupes:
        typer.secho(f"\n📋 Found {len(dupes)} groups of duplicates:", fg=typer.colors.YELLOW)
        for hash_val, files in dupes.items():
            typer.echo(f"\nHash: {hash_val[:16]}...")
            for file in files:
                typer.echo(f"  - {file}")
    else:
        typer.secho("✅ No duplicates found!", fg=typer.colors.GREEN)


@app.command()
def stats(path: Path = typer.Argument(..., help="Directory path to analyze")):
    """Show folder statistics by category."""
    if not path.exists() or not path.is_dir():
        typer.secho(f"Error: {path} is not a valid directory", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"📊 Analyzing: {path}", fg=typer.colors.CYAN)
    stats_analyzer = FolderStats(config)
    statistics = stats_analyzer.get_statistics(path)
    
    typer.secho("\n📈 Statistics by Category:", fg=typer.colors.CYAN, bold=True)
    for category, data in statistics['by_category'].items():
        typer.echo(f"\n{category}:")
        typer.echo(f"  Files: {data['count']}")
        typer.echo(f"  Size: {data['size_human']}")
    
    typer.secho(f"\n📦 Total Files: {statistics['total_files']}", fg=typer.colors.GREEN)
    typer.secho(f"💾 Total Size: {statistics['total_size_human']}", fg=typer.colors.GREEN)


@app.command()
def watch(path: Path = typer.Argument(..., help="Directory path to watch")):
    """Watch folder and auto-organize new files."""
    if not path.exists() or not path.is_dir():
        typer.secho(f"Error: {path} is not a valid directory", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"👀 Watching: {path}", fg=typer.colors.CYAN)
    typer.secho("Press Ctrl+C to stop...", fg=typer.colors.YELLOW)
    
    watcher = FolderWatcher(path, config)
    try:
        watcher.start()
    except KeyboardInterrupt:
        typer.secho("\n⏹️  Stopped watching", fg=typer.colors.YELLOW)


@app.command()
def undo():
    """Undo the last organize operation."""
    typer.secho("↩️  Undoing last operation...", fg=typer.colors.CYAN)
    result = history.undo_last()
    
    if result['success']:
        typer.secho(f"✅ Reverted {result['reverted']} files!", fg=typer.colors.GREEN)
    else:
        typer.secho(f"❌ {result['message']}", fg=typer.colors.RED)


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    app()
