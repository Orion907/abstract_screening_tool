"""
Batch Processor

Manages batch processing of large abstract sets with progress tracking and error recovery.
Simplified for demo with basic batch management and progress tracking.
"""

from typing import List, Dict, Any, Optional, Callable
import time
import math

from ..data.models import Abstract, ScreeningResult, PICCriteria


class BatchProcessor:
    """
    Manages batch processing of abstracts for efficient screening.
    
    Demo version handles basic batch sizing and progress tracking.
    """
    
    def __init__(self, batch_size: int = 10, delay_between_batches: float = 1.0):
        """
        Initialize batch processor.
        
        Args:
            batch_size: Number of abstracts to process in each batch
            delay_between_batches: Delay between batches in seconds
        """
        self.batch_size = batch_size
        self.delay_between_batches = delay_between_batches
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'errors': 0,
            'start_time': None,
            'current_batch': 0,
            'total_batches': 0
        }
    
    def process_in_batches(self, 
                          abstracts: List[Abstract],
                          screening_function: Callable[[List[Abstract]], List[ScreeningResult]],
                          progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> List[ScreeningResult]:
        """
        Process abstracts in batches with progress tracking.
        
        Args:
            abstracts: List of abstracts to process
            screening_function: Function to process each batch
            progress_callback: Optional callback for progress updates
            
        Returns:
            List[ScreeningResult]: Combined results from all batches
        """
        if not abstracts:
            return []
        
        # Initialize processing stats
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'errors': 0,
            'start_time': time.time(),
            'current_batch': 0,
            'total_batches': math.ceil(len(abstracts) / self.batch_size)
        }
        
        all_results = []
        
        # Process in batches
        for i in range(0, len(abstracts), self.batch_size):
            batch_abstracts = abstracts[i:i + self.batch_size]
            batch_number = (i // self.batch_size) + 1
            
            self.processing_stats['current_batch'] = batch_number
            
            try:
                # Process current batch
                batch_results = screening_function(batch_abstracts)
                all_results.extend(batch_results)
                
                # Update statistics
                self.processing_stats['total_processed'] += len(batch_abstracts)
                self.processing_stats['successful'] += sum(
                    1 for r in batch_results if r.decision.value != 'Error'
                )
                self.processing_stats['errors'] += sum(
                    1 for r in batch_results if r.decision.value == 'Error'
                )
                
                # Call progress callback if provided
                if progress_callback:
                    progress_info = self._get_progress_info(len(abstracts))
                    progress_callback(progress_info)
                
                # Add delay between batches (except for the last batch)
                if batch_number < self.processing_stats['total_batches']:
                    time.sleep(self.delay_between_batches)
                    
            except Exception as e:
                # Handle batch processing error
                error_message = f"Batch {batch_number} processing failed: {str(e)}"
                
                # Create error results for all abstracts in the failed batch
                for abstract in batch_abstracts:
                    error_result = ScreeningResult.create_error_result(
                        abstract.reference_id,
                        error_message
                    )
                    all_results.append(error_result)
                
                # Update error statistics
                self.processing_stats['total_processed'] += len(batch_abstracts)
                self.processing_stats['errors'] += len(batch_abstracts)
                
                # Call progress callback for failed batch
                if progress_callback:
                    progress_info = self._get_progress_info(len(abstracts))
                    progress_info['last_error'] = error_message
                    progress_callback(progress_info)
        
        return all_results
    
    def _get_progress_info(self, total_abstracts: int) -> Dict[str, Any]:
        """
        Get current progress information.
        
        Args:
            total_abstracts: Total number of abstracts being processed
            
        Returns:
            Dict containing progress information
        """
        current_time = time.time()
        elapsed_time = current_time - self.processing_stats['start_time']
        
        # Calculate processing rate
        if elapsed_time > 0:
            processing_rate = self.processing_stats['total_processed'] / elapsed_time
        else:
            processing_rate = 0
        
        # Estimate remaining time
        remaining_abstracts = total_abstracts - self.processing_stats['total_processed']
        if processing_rate > 0:
            estimated_remaining_time = remaining_abstracts / processing_rate
        else:
            estimated_remaining_time = 0
        
        # Calculate completion percentage
        completion_percentage = (self.processing_stats['total_processed'] / total_abstracts) * 100
        
        return {
            'current_batch': self.processing_stats['current_batch'],
            'total_batches': self.processing_stats['total_batches'],
            'total_processed': self.processing_stats['total_processed'],
            'total_abstracts': total_abstracts,
            'successful': self.processing_stats['successful'],
            'errors': self.processing_stats['errors'],
            'completion_percentage': completion_percentage,
            'elapsed_time': elapsed_time,
            'estimated_remaining_time': estimated_remaining_time,
            'processing_rate': processing_rate
        }
    
    def optimize_batch_size(self, total_abstracts: int, target_duration_minutes: int = 10) -> int:
        """
        Optimize batch size based on total abstracts and target duration.
        
        Args:
            total_abstracts: Total number of abstracts to process
            target_duration_minutes: Target duration for processing in minutes
            
        Returns:
            int: Optimized batch size
        """
        # Estimate processing time per abstract (demo assumption: 2 seconds per abstract)
        estimated_time_per_abstract = 2.0
        
        # Calculate target abstracts per minute
        target_abstracts_per_minute = total_abstracts / target_duration_minutes
        
        # Calculate optimal batch size (considering API rate limits)
        # Demo assumption: API can handle 10 requests per minute
        max_batch_size = min(50, total_abstracts)  # Cap at 50 for demo
        min_batch_size = max(1, min(5, total_abstracts))  # Minimum 1, usually 5
        
        # Calculate based on target duration
        calculated_batch_size = max(min_batch_size, min(max_batch_size, 
                                                       int(target_abstracts_per_minute / 6)))
        
        return calculated_batch_size
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get summary of the last processing run.
        
        Returns:
            Dict containing processing summary
        """
        if self.processing_stats['start_time'] is None:
            return {'status': 'No processing run completed yet'}
        
        total_time = time.time() - self.processing_stats['start_time']
        
        return {
            'total_processed': self.processing_stats['total_processed'],
            'successful': self.processing_stats['successful'],
            'errors': self.processing_stats['errors'],
            'total_batches': self.processing_stats['total_batches'],
            'total_time_seconds': total_time,
            'average_time_per_abstract': total_time / self.processing_stats['total_processed'] if self.processing_stats['total_processed'] > 0 else 0,
            'success_rate': (self.processing_stats['successful'] / self.processing_stats['total_processed']) * 100 if self.processing_stats['total_processed'] > 0 else 0,
            'error_rate': (self.processing_stats['errors'] / self.processing_stats['total_processed']) * 100 if self.processing_stats['total_processed'] > 0 else 0
        }
    
    def estimate_processing_time(self, total_abstracts: int) -> Dict[str, Any]:
        """
        Estimate processing time for a given number of abstracts.
        
        Args:
            total_abstracts: Number of abstracts to process
            
        Returns:
            Dict containing time estimates
        """
        # Demo estimates based on typical LLM API response times
        estimated_time_per_abstract = 2.0  # seconds
        
        # Account for batch delays
        total_batches = math.ceil(total_abstracts / self.batch_size)
        batch_delay_time = (total_batches - 1) * self.delay_between_batches
        
        # Calculate estimates
        processing_time = total_abstracts * estimated_time_per_abstract
        total_time = processing_time + batch_delay_time
        
        return {
            'total_abstracts': total_abstracts,
            'estimated_processing_time_seconds': processing_time,
            'estimated_batch_delay_seconds': batch_delay_time,
            'estimated_total_time_seconds': total_time,
            'estimated_total_time_minutes': total_time / 60,
            'total_batches': total_batches,
            'batch_size': self.batch_size
        }
    
    def reset_stats(self):
        """Reset processing statistics."""
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'errors': 0,
            'start_time': None,
            'current_batch': 0,
            'total_batches': 0
        }