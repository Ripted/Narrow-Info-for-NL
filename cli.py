#!/usr/bin/env python3
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import sys

console = Console()

def fetch_level_details(level_id):
    url = f"https://api.narrowarrow.xyz/level-details/{level_id}?isCustomLevel=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[dim red]Error fetching level details: {e}[/dim red]")
        return None

def fetch_leaderboard(level_id):
    url = f"https://api.narrowarrow.xyz/leaderboard?levelId={level_id}"
    
    try:
        console.print(f"[cyan]Fetching leaderboard for level {level_id}...[/cyan]")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching leaderboard: {e}[/red]")
        return None

def fetch_run_details(run_id):
    url = f"https://api.narrowarrow.xyz/runs/{run_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def format_time(seconds):
    """Format time from seconds to readable format (seconds.milliseconds)"""
    if seconds is None:
        return "N/A"
    
    return f"{seconds:.3f}s"

def display_level_info(level_details):
    """Display level information header"""
    if not level_details:
        return
    
    level_info = level_details.get('levelInfo', {})
    name = level_info.get('name', 'Unknown')
    author = level_info.get('author', 'Unknown')
    created_at = level_info.get('created_at', 'N/A')
    likes = level_info.get('like_count', 0)
    
    if isinstance(created_at, str) and 'T' in created_at:
        created_at = created_at.split('T')[0]
    
    info_text = f"[bold white]{name}[/bold white]\n"
    info_text += f"[dim]Created by:[/dim] [green]{author}[/green]  "
    info_text += f"[dim]|[/dim]  [dim]Created:[/dim] [cyan]{created_at}[/cyan]  "
    info_text += f"[dim]|[/dim]  [dim]Likes:[/dim] [yellow]{likes}[/yellow]"
    
    console.print(Panel(info_text, box=box.ROUNDED, border_style="blue"))

def convert_leaderboard_to_list(leaderboard_data):
    """Convert leaderboard data (dict or list) to a list of run entries"""
    runs = []
    
    if isinstance(leaderboard_data, list):
        runs = leaderboard_data
    elif isinstance(leaderboard_data, dict):
        # Try to extract from numbered keys (0, 1, 2, ...)
        for key in sorted(leaderboard_data.keys(), key=lambda x: int(x) if str(x).isdigit() else float('inf')):
            if str(key).isdigit():
                runs.append(leaderboard_data[key])
    
    return runs

def display_leaderboard_table(leaderboard_data, level_id):
    """Display leaderboard in a formatted table"""
    runs = convert_leaderboard_to_list(leaderboard_data)
    
    if not runs:
        console.print("[yellow]No runs found for this level[/yellow]")
        return
    
    # Fetch run details to get finishedAt timestamps
    console.print(f"[cyan]Fetching run details for {len(runs)} runs...[/cyan]")
    run_details_map = {}
    for idx, run in enumerate(runs, 1):
        if isinstance(run, dict):
            run_id = run.get('run_id')
            if run_id:
                console.print(f"[dim]Fetching run {idx}/{len(runs)}...[/dim]", end="\r")
                details = fetch_run_details(run_id)
                if details:
                    run_details_map[run_id] = details
    
    console.print(" " * 50, end="\r")  # Clear the message
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Rank", justify="center", style="cyan", width=6)
    table.add_column("Player", justify="left", style="green", width=20)
    table.add_column("Time", justify="right", style="white", width=12)
    table.add_column("Arrow", justify="left", style="yellow", width=15)
    table.add_column("Finished At", justify="left", style="dim", width=19)
    table.add_column("Run ID", justify="left", style="dim", width=10)
    
    for idx, run in enumerate(runs, 1):
        if not isinstance(run, dict):
            continue
            
        username = run.get('username', 'Unknown')
        completion_time = run.get('completion_time')
        arrow_name = run.get('arrow_name', 'N/A')
        run_id = run.get('run_id', 'N/A')
        
        # Get finishedAt from run details
        finished_at = 'N/A'
        if run_id in run_details_map:
            finished_at_raw = run_details_map[run_id].get('finishedAt', 'N/A')
            if isinstance(finished_at_raw, str) and 'T' in finished_at_raw:
                # Format: "2025-05-04T08:18:45.000Z" -> "2025-05-04 08:18:45"
                finished_at = finished_at_raw.split('.')[0].replace('T', ' ')
            else:
                finished_at = str(finished_at_raw)
        
        table.add_row(
            str(idx),
            username,
            format_time(completion_time),
            arrow_name,
            finished_at,
            str(run_id)
        )
    
    console.print(table)
    console.print(f"\n[dim]Total runs: {len(runs)}[/dim]")

def process_level(level_id):
    """Process a level: fetch level details and leaderboard, then display"""
    # Fetch level details
    console.print(f"[dim]Fetching level details...[/dim]")
    level_details = fetch_level_details(level_id)
    
    # Fetch leaderboard
    leaderboard_data = fetch_leaderboard(level_id)
    
    if not leaderboard_data:
        console.print(f"[red]Failed to fetch leaderboard for level {level_id}[/red]")
        return
    
    console.print()
    
    # Display level info
    if level_details:
        display_level_info(level_details)
    
    # Display leaderboard
    display_leaderboard_table(leaderboard_data, level_id)

def main():
    console.print(Panel(
        "[bold green]Narrow Arrow Leaderboard Viewer[/bold green]",
        subtitle="api.narrowarrow.xyz",
        box=box.DOUBLE_EDGE
    ))
    
    # Handle command-line argument for first level
    if len(sys.argv) > 1:
        level_id = sys.argv[1]
        process_level(level_id)
        console.print()
    
    # Interactive loop
    while True:
        level_id = console.input("\n[cyan]Enter level ID (or press Enter to quit): [/cyan]")
        
        if not level_id:
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        if level_id.lower() in ['quit', 'exit', 'q']:
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        process_level(level_id)
        console.print()

if __name__ == "__main__":
    main()
